# AurumWaveAPI Project Setup

This repository contains a script for starting a Django Backend server for AurumWave. It includes both Linux/MacOS and Windows
versions.

## Prerequisites

- Python 3.x installed on your system
- `pip` package manager installed

## Files

- `run.sh`: Script to set up and run the Django server on Linux/MacOS
- `run.bat`: Script to set up and run the Django server on Windows

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/myousafmalik/AurumWaveAPI.git
cd AurumWaveAPI
```

### 2. Run the Script

#### For Linux/MacOS

Make sure the script has execute permission:

```bash
chmod +x run.sh
```

Then, run:

```bash
./run.sh
```

#### For Windows

Simply double-click run.bat or run it from the Command Prompt:

```batch
run.bat
```

### 3. Access the Django Server

By default, the server will be accessible at:

```arduino
http://127.0.0.1:8000
```

## Notes

If the venv folder is not found, the script will create a virtual environment automatically.
All necessary packages will be installed from requirements.txt.
The server will start using the default Django settings.

## Stopping the Server

For Linux/MacOS: Press Ctrl + C in the terminal.
For Windows: Press Ctrl + C in the Command Prompt.