# Google Calendar Team Report

Generate insights on number of hours in meetings per team and team member.

## Getting Started

```bash
virtualenv .virtualenv
source .virtualenv/bin/activate
pip install -r requirements.txt
```

## Configuration

First, you need to create a [Google API Project](https://console.developers.google.com/project), and then create a [Google API Credential OAuth client ID](https://console.developers.google.com/apis/credentials). Make sure to use the Redirect URI `http://localhost:8080/`.

```bash
./run.sh init  # create local config store
./run.sh login  # authenticate to Google cal, will pop up a web browser window
./run.sh list  # list all the available calendars
./run.sh add --team DATA --id cseibert@hearsaycorp.com  # run this for each person. you are creating a list called "DATA"
./run.sh dump --team DATA  # show the raw meetings/day data
./run.sh report --team DATA  # generate a summary
./run.sh csv --team DATA --output ~/Desktop/team_data.csv  # output raw data
./run.sh top --team DATA  # show top meetings for the team
```

*Note: once you get rolling, it may be easier to hand-edit the config file at `~/.gcal-report`.*

## Example output

For the dump:

```bash
          date  meeting_hours  meeting_min
0   2014-12-22       2.500000          150
1   2014-11-26       0.050000            3
2   2015-01-14       1.933333          116
3   2014-11-24       1.616667           97
4   2014-11-07       4.866667          292
5   2015-01-21       9.750000          585
6   2015-01-12       0.433333           26
7   2014-12-10       0.366667           22
8   2015-01-07       1.000000           60
9   2014-11-05       0.750000           45
10  2014-12-08       2.750000          165
11  2014-11-28       1.000000           60
12  2015-01-20       3.616667          217
13  2015-01-01       1.000000           60
14  2014-12-12       1.116667           67
15  2014-12-02       0.250000           15
16  2015-01-05       3.550000          213
17  2014-11-13       0.500000           30
18  2015-01-26       0.366667           22
19  2014-12-29       0.366667           22
20  2014-11-19       1.000000           60
21  2015-01-23       5.250000          315
22  2015-01-28       1.750000          105
23  2014-12-19       5.866667          352
24  2014-11-17       3.000000          180
25  2015-02-01       1.500000           90
26  2014-12-04       0.116667            7
27  2014-12-17       2.616667          157
28  2015-01-30       1.500000           90
29  2014-11-21       5.000000          300
30  2015-01-22       0.116667            7
31  2015-01-15       2.366667          142
32  2014-12-11       0.500000           30
33  2014-11-25       1.000000           60
34  2015-01-19       1.550000           93
35  2014-11-10       0.366667           22
36  2015-01-16       1.116667           67
37  2014-12-15       2.616667          157
38  2014-12-13       3.000000          180
39  2014-12-26       1.000000           60
40  2014-11-14       2.750000          165
41  2014-12-03       1.200000           72
42  2015-01-02       1.000000           60
43  2015-01-08       4.200000          252
44  2014-12-09       1.866667          112
45  2014-12-01       3.750000          225
46  2014-11-18       9.000000          540
47  2015-01-29       1.183333           71
48  2015-01-06       1.966667          118
49  2014-12-05       3.866667          232
50  2014-12-18       3.366667          202
51  2015-01-27       1.000000           60
52  2015-02-02       1.500000           90
53  2015-01-09       3.616667          217
54  2015-01-13       0.750000           45
55  2014-12-16       0.116667            7
56  2014-11-20       1.933333          116
```

For the report:

```bash
       meeting_hours  meeting_min
count      57.000000    57.000000
mean        2.141813   128.508772
std         2.009423   120.565353
min         0.050000     3.000000
25%         1.000000    60.000000
50%         1.500000    90.000000
75%         3.000000   180.000000
max         9.750000   585.000000
```

*Note: overlapping meetings are double-counted.*
