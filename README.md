# ADHDBot-Slack

This is a starting point for implementation of a bot for an
ADHD-related channel on a slack.com site.  As such, its chances
of ever seeing completion are slim but perhaps if published here
it's less likely to be forgotten. 🙈

## Goals:

* Provide an interface for 35 minute coworking sessions for channel 
members.
* Robust connectivity
* Configuration tool
* Eventually rename
* Modularize to allow use in different channels

## Using:

At present, there is no configuration tool and no main script to 
execute.  This provides only a library and no instructions for now.

## Python dependencies:

Python 3.4 and the following packages (all pip installable):

* slacker
* websocket-client
* sqlalchemy