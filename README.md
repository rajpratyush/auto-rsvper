# Meetup auto-RSVP

## Problem Statement

Language: Any

Must work in: Linux

This task is relatively simple (in theory), but it will help us assess your code organization abilities.

Write a program for meetup.com that sends an auto-RVSP to specific groups. For example, suppose you are a member of 7 different Meetup groups, some of which have very popular events that fill up quickly. You want to sign up for them as fast as possible to ensure that you get a spot.

Your program needs take care of authentication, searching for events in configured groups (not all), and automatically signing up on the user's behalf in a timely manner. Usage of existing Meetup client libraries is permitted.

It's OK for your program to be a simple command-line tool that needs to be run from cron once an hour or something like that.

## Seting Up
1. Fire the following commands in terminal to create a virtual environment and install the dependencies.
- python3 -m virtualenv ccextractor_env
- source ccextractor_env/bin/activate
- pip3 install -r requirements.txt

2. Ensure that you have the username and password of Meetup.com present in your path
- export MEETUP_USERNAME=`user` 
- export MEETUP_PASSWORD=`pass`

3. Run `groups.py` thereby generating `groups.json`

``` shell
python3 groups.py 
```
This generated `groups.json` has the groups that you want to auto-RSVP.

4. Run `rsvp.py` inorder to RSVP all events available for the selected gropus.
``` shell
python3 rsvp.py 
```

### Proposed Solution has been tested only on `Ubuntu 19.10` and with Python 3.7.4
