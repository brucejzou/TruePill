# True Pill Server

## Setup
Install dependencies
`pip install -r requirements.txt`

## Running
### Unix
```
$ export FLASK_APP=api.py
$ flask run
```

### Windows PowerShell
```
PS C:\path\to\app> $env:FLASK_APP = "hello.py"
PS C:\path\to\app> flask run
```
If `flask run` doesn't work, an alternative is `python -m flask run`.

The server will run locally at http://127.0.0.1:5000/
