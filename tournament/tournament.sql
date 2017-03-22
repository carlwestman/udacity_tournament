-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.


-- Creates tournament table in order to support multiple tournaments
    -- Table Structure:
        -- tournament_id, type = serial (int), primary_key
        -- tournament_name, type = text
        -- winner_id, type = int, foreign key --> player(id), default NULL
CREATE TABLE tournament (
    tournament_id SERIAL PRIMARY KEY,
    tournament_name TEXT,
    winner INT DEFAULT NULL
    );

-- Creates players table in order to keeptrack of users
    -- Table structure:
        -- player_id, type =  serial, primary_key
        -- player_name, type = text
CREATE TABLE players (
    player_id SERIAL PRIMARY KEY,
    player_name TEXT
    );

-- CREATE tournament_participants to keep track of players in given tournament
    -- Table structure
        -- tournament_id, int, foreign_key to tournament(tournament_id)
        -- player_id, int, foreign_key to players(player_id)
        -- PRIMARY_KEY on (tournament_id, player_id)
CREATE TABLE tournament_participants (
    tournament_id INTEGER REFERENCES tournament(tournament_id),
    player_id INTEGER REFERENCES players(player_id),
    PRIMARY KEY (tournament_id, player_id)
    );

-- CREATE matches table
-- Keep track of matches in given tournament, both who played who and who won
    -- Table structure
        -- match_id, int, primary_key
        -- Tournament_id, int, foreign_key to tournament(tournament_id)
        -- winner, int, foreign_key to player(player_id)
        -- loser, int, foreign_key to player(player_id)
CREATE TABLE matches (
    match_id SERIAL PRIMARY KEY,
    tournament_id INTEGER REFERENCES tournament(tournament_id),
    winner INTEGER REFERENCES players(player_id),
    loser INTEGER REFERENCES players(player_id)
    );


-- Create match_summary view to easily be able to access summary of matches played
-- View calculated from matches table and player table
    -- View structure:
        -- Tournament_id, int, from matches table
        -- player_id, int, from players table
        -- wins, int, from matches table
        -- matches, int,
---TODO: Make This query better and more scalable...
CREATE VIEW matches_summary AS
SELECT
    t.tournament_id,
    t.player_id,
    p.player_name,
    COALESCE(u.wins,0) as wins,
    COALESCE(u.matches,0) as matches
FROM tournament_participants t JOIN players p
ON t.player_id = p.player_id
LEFT JOIN
    (
    SELECT
        tournament_id,
        player_id,
        sum(count_wins) as wins,
        sum(count_wins + count_losses) as matches
    FROM
        (
        SELECT
            tournament_id,
            winner as player_id,
            count(*) as count_wins,
            0 as count_losses
        from matches
        group by tournament_id, winner
        union all
        SELECT
            tournament_id,
            loser as player_id,
            0 as count_wins,
            count(*) as count_losses
        from matches
        group by tournament_id, loser
        ) as ugly
    GROUP BY Tournament_id, player_id
    ) as u
ON t.tournament_id = u.tournament_id
AND t.player_id = u.player_id
ORDER BY tournament_id, wins;





