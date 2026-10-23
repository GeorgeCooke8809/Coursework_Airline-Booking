Make sure you have already synced your uv virtual environment with developer dependencies (```uv sync```). Then

To run basic unit tests:
``` POWERSHELL
uv run pytest -vv
```


To get more detailed logging statements:
``` POWERSHELL
uv run pytest --log-cli-level=DEBUG  
```


To test a specific function: 
``` POWERSHELL
uv run pytest tests/test_get_all_routes.py -vv
```