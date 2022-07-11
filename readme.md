# EQ Bot

## Features
    - Perform regular guild dumps and notify remote discord channel of members who have logged on, logged off, joined the guild, or left the guild.
    - Observable log parser which can notify subscribed python functions when specific types of messages arrive.

## Installation (Windows)

1. Install Python3.7+
1. (If using Powershell) Run the below command in Powershell as Adminsitrator to allow for execution of Python modules:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```
1. Clone down the repository locally
1. From within a terminal (Powershell, bash, etc), navigate to the cloned repository
1. Create and activate a new virtual environment
```powershell
python -m venv .venv
.\.venv\Scripts\activate
```
1. Install dependencies
```powershell
pip install -r requirements.txt
```

## Configuration
The `config.yaml` at the project root can be used to change the bot's default behavior.

### Properties
Coming soon. Refer to example properties for now.

## Execution

1. Activate the virtual environment
```powershell
.\.venv\Scripts\activate
```

1. Run the bot
```powershell
python .\eq_bot\main.py
```
