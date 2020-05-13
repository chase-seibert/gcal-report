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

```bash
./run.sh list
```

## Configuration

You need to define teams of people to report on.

Update the `settings.py` file:

```python
DOMAIN = '@example.com'

TEAMS = {
    'team1': [
        'user1',
        'user2',
    ],
}
```

Teams can be named whatever you want. The user values should map to Google Apps
user IDs, which are email addresses. If you want to omit the domain on each one,
use the `DOMAIN` setting to set the default suffix.

## Run Reports

Show the raw meetings/day data:

```
>./run.sh dump --team team1
                           user1    summary
2020-02-13                 355.0    355.0
2020-02-14                 245.0    245.0
2020-02-15                   0.0      0.0
2020-02-16                   0.0      0.0
2020-02-17                  30.0     30.0
2020-02-18                 335.0    335.0
2020-02-19                 150.0    150.0
2020-02-20                 355.0    355.0
2020-02-21                 330.0    330.0
```

Generate a summary:
```
>./run.sh report --team team1
                      user1     summary
count             90.000000   90.000000
mean             180.500000  180.500000
std              143.411583  143.411583
min                0.000000    0.000000
25%                0.000000    0.000000
50%              210.000000  210.000000
75%              292.500000  292.500000
max              495.000000  495.000000
```

Count is the number of days. All other numbers are minutes.

Save raw data:
```
>./run.sh csv --team team1 --output ~/Desktop/team_data.csv
```

Show the top meetings:
```
>./run.sh top --team team1 --limit 10
meeting 1 (120)
meeting 2 (60)
```
