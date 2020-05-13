# Google Calendar Team Report

Generate insights on number of hours in meetings per team and team member.

## Getting Started

```bash
virtualenv .virtualenv
source .virtualenv/bin/activate
pip install -r requirements.txt
```

## Authenticate

First, you need to create a [Google API Project](https://console.developers.google.com/project), and then create a [Google API Credential OAuth client ID](https://console.developers.google.com/apis/credentials). Make sure to use the Redirect URI `http://localhost:8080/`.

Then, authenticate to the Google calendar API. This will pop up a web browser window:

```bash
./run.sh login  
```

After login, your credentials are stored at `~/.gcal-report-creds`

You can test your login credentials with:

```
./run.sh list
```

## Configuration

First, you need to define teams of people to report on.

Update the `settings.py` file:

```
DOMAIN = '@example.com'

TEAMS = {
    'team1': [
        'user1',
        'user2',
    ],
}
```

## Run Reports

Show the raw meetings/day data:

```
>./run.sh dump --team team1
date  meeting_hours  meeting_min
0   2014-12-22       2.500000          150
1   2014-11-26       0.050000            3
2   2015-01-14       1.933333          116
3   2014-11-24       1.616667           97
4   2014-11-07       4.866667          292
5   2015-01-21       9.750000          585
```

Generate a summary:
```
>./run.sh report --team team1
```

Output raw data:
```
>./run.sh csv --team team1 --output ~/Desktop/team_data.csv
```

Show the top meetings:
```
>./run.sh top --team team1
```
