-------------------------------------------------------------------------------
-- File: tournament.sql
-- Author: Juana De La Cuesta

-- Table definitions for the tournament project.
-------------------------------------------------------------------------------
DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament

-- In order to by able to pair an uneven number of players, the 0 value will
-- be reserved to indicate a player is getting a free win because there is no 
-- opponent available, so the players IDs must start in 1.
CREATE SEQUENCE ID_seq 
  START WITH 1
  INCREMENT BY 1;
 
--Table to storage all the tournaments data
CREATE TABLE IF NOT EXISTS tournaments (
    tournament_ID integer DEFAULT nextval('ID_seq') PRIMARY KEY,
    name text NOT NULL
    );

INSERT INTO tournament (tournament_ID, name) VALUES (0, 'reserved');
    
 --Table to storage all players information
CREATE TABLE IF NOT EXISTS players( 
    player_ID  integer DEFAULT nextval('ID_seq') PRIMARY KEY,
    tournament_ID integer REFERENCES tournaments(tournament_ID) NOT NULL,
    name text NOT NULL,
    UNIQUE (player_ID, tournament_ID)
    );
    
--Table to storage all matches results
CREATE TABLE IF NOT EXISTS matches(
    match_ID serial,
    winner_ID integer REFERENCES players(player_ID) NOT NULL,
    loser_ID integer REFERENCES players(player_ID) CHECK(winner_ID != loser_ID),
    tie boolean, 
	PRIMARY KEY (winner_ID, loser_ID)
    );    

--View to get all the matches played by every player    
CREATE VIEW games AS SELECT player_ID, name, tournament_ID, COUNT(match_ID) 
AS games FROM players LEFT JOIN matches ON (player_ID = matches.winner_ID OR 
player_ID = matches.loser_ID) GROUP BY player_ID, tournament_ID;

--View to get all the wins of every players
CREATE VIEW wins AS SELECT player_ID, COUNT(winner_ID) AS wins 
FROM players LEFT JOIN matches ON player_ID = winner_ID AND tie = False 
GROUP BY players.player_ID;

CREATE VIEW standings AS SELECT games.player_ID, name, wins, games FROM 
games, wins WHERE wins.player_ID = games.player_ID ORDER BY wins DESC;

        