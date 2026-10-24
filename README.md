Made by George A.C. Cooke (2026/27)

GitHub: GeorgeCooke8809/Coursework_Airline-Booking

Built and tested with Python 3.14

## The Brief
I have started developing this project for my A-Level Computer Science coursework under the Eduqas exam board. We are given relative free reign over what we do as long as it is a database project. I have decided to make a route management and booking system for a fictional airline (Infinity Airways).

## Requirements:
- Python 3.14
- UV

## Installing UV (if required):

``` powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Setup & Execution

### 1. Install all dependencies

``` powershell
uv sync
```
To install all dependencies including dev dependencies (e.g.: pytest).

##### Alternatively:
``` POWERSHELL
uv sync --no-dev
```
To install without dev dependencies.

### 2. Create databases
Please check ```/data```, you should see a file ```data.db``` and another file ```test_data.db```. ```data.db``` is used in the main app and ```test_data.db``` is used for unit tests. If you do not see this, please run
``` POWERSHELL
uv run alembic upgrade head
```
then duplicate the created ```data.db``` file and rename it to ```test_data.db```.

If these files are already present, skip straight to step 3.

### 3. Run the unit tests
One ought to run the unit tests to ensure all is running as it should before trying the GUI. Run using:
``` POWERSHELL
uv run pytest -vv
```
If any tests fail, proceed to troubleshooting. Otherwise, continue to step 4.

### 4. Run the app
``` powershell
uv run run.py
```

## Troubleshooting:
### 1 - Unit Test Troubleshooting:
#### 1.1 - Most Common Issues:
##### 1.1.1 - OperationalError with "no such table: ..."
The error report may say:
```FAILED tests/test_create_route.py::test_add_valid_route_valid_price - sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: airports``` (or a variation of it with another function).

The specific part we are looking for is "no such table: ..."

If this error occurs for many functions being tested, indicates that the test database was not present. To correct, please check ```/data```. This should have a ```data.db``` file and a ```test_data.db``` file. If unit tests are run without a ```test_data.db``` file, and empty one will automatically be created (we don't want this). Please run:
``` POWERSHELL
uv run alembic upgrade head
```
to create ```data.db```. Please then duplicate this file and rename it to ```test_data.db```.

#### 1.2 - test_create_route
##### 1.2.1 - InvalidAirportException
This indicates that the EGLL (Heathrow) and KJFK (JFK) airports are not present in the database. This would be symptomatic of none of the airports being present to populate the airports table please run:
``` POWERSHELL
uv run "/.devtools/add-airports/add_airports.py"
```

#### 1.3 - test_get_all_routes
##### 1.3.1 - InvalidAirportException
This happens as routes have to be created before routes can be retrieved, one would expect it to appear in other functions too. Please see 1.2.1.

#### 1.4 - test_add_schedule
##### 1.4.1 - InvalidAirportException
This happens as a route has to be created before schedules can be created, one would expect it to appear in other functions too. Please see 1.2.1.