"""Dev tool to populate the airports table from airports_seed.json.

Run from the repository root:
    uv run .devtools/add-airports/add_airports.py [options]

Use --help to see all available options.
"""

import argparse
import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent

# Allows the project's models package to be imported no matter where the script is run from
sys.path.insert(0, str(REPO_ROOT))

from sqlalchemy import create_engine, insert, inspect, select, update

from models import Airport
from models.base import DB_PATH

DEFAULT_SEED_PATH = SCRIPT_DIR / "airports_seed.json"
REQUIRED_FIELDS = ["icao", "iata", "name", "city", "country", "latitude", "longitude", "timezone"]


def parse_args() -> argparse.Namespace:
    """Parses the command line arguments for the script.

    Returns:
        argparse.Namespace: The parsed arguments
    """

    parser = argparse.ArgumentParser(description="Populate the airports table from a JSON seed file.")
    parser.add_argument("--file", type=Path, default=DEFAULT_SEED_PATH, help=f"Path to the seed JSON file (default: {DEFAULT_SEED_PATH.name})")
    parser.add_argument("--db", type=Path, default=DB_PATH, help="Path to the SQLite database (default: data/data.db)")
    parser.add_argument("--update", action="store_true", help="Overwrite airports that already exist with the seed values instead of skipping them")
    parser.add_argument("--limit", type=int, default=None, help="Only process the first N airports from the seed file")
    parser.add_argument("--country", type=str, default=None, help="Only add airports from this country (case insensitive, e.g. \"United Kingdom\")")
    parser.add_argument("--dry-run", action="store_true", help="Show what would happen without writing anything to the database")
    return parser.parse_args()


def load_seed(path: Path) -> list[dict]:
    """Loads and validates the airport records from the seed file.

    Args:
        path (Path): The path to the seed JSON file

    Returns:
        list[dict]: The list of airport records
    """

    if not path.exists():
        sys.exit(f"Seed file not found: {path}")

    with open(path, encoding="utf-8") as file:
        records = json.load(file)

    if not isinstance(records, list):
        sys.exit("Seed file must contain a JSON list of airports")

    for index, record in enumerate(records):
        missing = [field for field in REQUIRED_FIELDS if field not in record]
        if missing:
            sys.exit(f"Record {index} is missing fields: {', '.join(missing)}")

    return records


def main():
    args = parse_args()

    if not args.db.exists():
        sys.exit(f"Database not found: {args.db}\nRun the alembic migrations first (uv run alembic upgrade head)")

    records = load_seed(args.file)

    if args.country:
        records = [record for record in records if record["country"].lower() == args.country.lower()]
    if args.limit is not None:
        records = records[:args.limit]

    engine = create_engine(f"sqlite:///{args.db}")

    if not inspect(engine).has_table(Airport.__tablename__):
        sys.exit("The airports table does not exist. Run the alembic migrations first (uv run alembic upgrade head)")

    # Uses the table directly (SQLAlchemy Core) so the ORM relationships don't need to be configured
    airports_table = Airport.__table__

    added = 0
    updated = 0
    skipped = 0
    conflicts = []

    connection = engine.connect()
    transaction = connection.begin()

    try:
        # Loads existing airports once so each record doesn't need its own query
        existing_iata_by_icao = {row.icao: row.iata for row in connection.execute(select(airports_table.c.icao, airports_table.c.iata))}
        icao_by_iata = {iata: icao for icao, iata in existing_iata_by_icao.items() if iata}

        to_insert = []

        for record in records:
            icao = record["icao"].strip().upper()
            iata = record["iata"].strip().upper() if record["iata"] else None
            values = {
                "iata": iata,
                "name": record["name"],
                "city": record["city"],
                "country": record["country"],
                "latitude": float(record["latitude"]),
                "longitude": float(record["longitude"]),
                "timezone": record["timezone"],
            }

            # Stops an IATA code being given to two different airports, which would break the unique constraint
            if iata and iata in icao_by_iata and icao_by_iata[iata] != icao:
                conflicts.append(f"{icao}: IATA {iata} already used by {icao_by_iata[iata]}")
                continue

            if icao not in existing_iata_by_icao:
                to_insert.append({"icao": icao, **values})
                added += 1
            elif args.update:
                old_iata = existing_iata_by_icao[icao]
                if old_iata and old_iata != iata:
                    del icao_by_iata[old_iata]
                connection.execute(update(airports_table).where(airports_table.c.icao == icao).values(**values))
                updated += 1
            else:
                skipped += 1
                continue

            existing_iata_by_icao[icao] = iata
            if iata:
                icao_by_iata[iata] = icao

        # Inserts all new airports in a single executemany call
        if to_insert:
            connection.execute(insert(airports_table), to_insert)

        if args.dry_run:
            transaction.rollback()
        else:
            transaction.commit()
    except Exception:
        transaction.rollback()
        raise
    finally:
        connection.close()

    prefix = "[DRY RUN] Would have" if args.dry_run else "Done."
    print(f"{prefix} processed {len(records)} airports from {args.file.name}")
    print(f"  Added:     {added}")
    print(f"  Updated:   {updated}")
    print(f"  Skipped:   {skipped} (already in database{', use --update to overwrite' if skipped and not args.update else ''})")
    print(f"  Conflicts: {len(conflicts)}")
    for conflict in conflicts[:20]:
        print(f"    {conflict}")
    if len(conflicts) > 20:
        print(f"    ...and {len(conflicts) - 20} more")


if __name__ == "__main__":
    main()
