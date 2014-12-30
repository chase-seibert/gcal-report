# Google Calendar Team Report

Generate insights on number of hours in meetings per team and team member.

## Getting Started

```bash
virtualenv .virtualenv
source .virtualenv/bin/activate
pip install -r requirements.txt
```

## Configuration

First, you need to create a [Google API Project](https://console.developers.google.com/project). Make sure to use the Redirect URI `http://localhost:8080/`.

```bash
./run.sh init
./run.sh auth
```

## Adding Calendars

You can list your available Google Calendar IDs with the command: `gcal-report list`.

You need to configure your list of teams and team members with the `gcal-report add` command.

