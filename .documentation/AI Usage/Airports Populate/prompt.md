## Prompt:
Please make me a python script I can run using ``` uv run ...``` in /.devtools/add-airports to populate the database with the airports in the airports_seed.json file. It should be made in a single Python file and should populate the airports table I have already made. DO NOT edit any files other than the python script that you make. Once complete, give me instructions on how to call it and nay modifiers I can put in the script.

## Response:
I've written the script at .devtools/add-airports/add_airports.py. No other files were changed. I tested it on a copy of data.db: it added all 10,030airports, a second run skipped them all, and --update worked. Your real database still has 0 airports, so you need to run it yourself.

How to run it

Run it from the project root, in the same folder as pyproject.toml:

uv run .devtools/add-airports/add_airports.py

It uses your project's existing uv environment, so you don't need to install anything extra. When it finishes it prints how many airports were added,
updated, skipped and in conflict.

Options

| Option | What it does |
|---|---|
| --dry-run | Shows what would happen without writing anything to the database |
| --update | Overwrites airports that are already in the table with the values from the seed file. By default they are skipped, so running it twice is safe |
| --country "United Kingdom" | Only adds airports from that country (not case-sensitive) |
| --limit 100 | Only processes the first N airports in the seed file |
| --file path/to/other.json | Uses a different seed file (default: airports_seed.json next to the script) |
| --db path/to/other.db | Uses a different SQLite database (default: data/data.db) |
| --help | Lists all of the options |

You can combine them, for example:
``` POWERSHELL
uv run .devtools/add-airports/add_airports.py --country "United Kingdom" --dry-run
```

If two airports have the same IATA code, the script skips the second one and lists it under Conflicts, instead of crashing on the unique constraint.

Bug in your models

Testing found a bug in your existing models. Route has two foreign keys to airports (origin_icao and destination_icao). The relationships on
Airport.departures/arrivals and Route.origin/destination don't say which key each one uses. Because of that, SQLAlchemy throws an AmbiguousForeignKeysError
the first time the Airport model is used in a query or insert. Your Flask app will hit the same error.

I didn't edit the models, as you asked. Instead, the script writes to the table directly, which avoids the error. To fix the models, add foreign_keys= to
each relationship, for example:

``` PYTHON
departures: Mapped[list["Route"]] = relationship(back_populates="origin", foreign_keys="Route.origin_icao")
```

arrivals needs ```foreign_keys="Route.destination_icao"```, and the matching relationships in models/route.py need ```foreign_keys=[origin_icao]``` and
```foreign_keys=[destination_icao]```.

There's also a smaller mismatch: routes.origin_icao, routes.destination_icao and airport_staff.assigned_airport_icao are declared as String(3), but ICAO
codes are 4 characters. SQLite doesn't enforce string lengths, so nothing breaks now.
