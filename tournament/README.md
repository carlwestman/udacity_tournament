# Udacity_tournament project

This is the final project in the intro to Back-end within the into to
programming nano-degree and udacity.

It is a library of functions that can be used to hold a swiss-system
tournament.
More info on swiss-system tournament
can be found here [here](https://en.wikipedia.org/wiki/Swiss-system_tournament).

## Functionality overview
Lib contains a set of functions to run a swiss-style tournament. 
A tournament has a tournament_name and is assigned a tournament_id.
It is possible to register players, each player has a name and is assigend a player_id.
It is also possible to register a player in a tournament.
When a tournament is set up according to above it is possible to make match pairing by
calling the swisspairing function. It will return the match pairing according to the swiss-
style tournament rules.
A match result is reported by calling the reportMatch function.

Detailed documentation over functions in code.

## Requirements:
* psycopg2 (standard in python)
* types (standard in python)

## Setup
* create database called `tournament`
    * If database requires authentication in connection, modify connect()
    function in tournament.py
* Run `tournament.sql` to setup tables

## Testing
* run `tournament_test.py`

