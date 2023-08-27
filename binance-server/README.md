# binance-server

A web server for binance.

## Usage

### Step 1 - Make The Virtual Environment

Create the virtual environment. I used Python 3.11.

```bash
binance-server $ python3.11 -m venv .venv
```

### Step 2 - Install the Packages

First activate the virtual environment, then install the packages
with poetry.

```bash
binance-server $ . .venv/bin/activate
(.venv) binance-server $ poetry install
```

### Step 3 - Run The Server

The poetry installation phase created a script that can be used to start the server.

```bash
(.venv) binance-server $ ./.venv/bin/start-binance-server
```

If you prefer to run it from visual studio code, there is a launch configuration
called "Start Server".
