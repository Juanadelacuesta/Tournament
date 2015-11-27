-------------------------------------------------------------------------------
-- File: tournament.sql
-- Author: Juana De La Cuesta

-- Table definitions for the tournament project.
-------------------------------------------------------------------------------

--Table to storage all players information
CREATE TABLE IF NOT EXISTS players (
    player_ID serial PRIMARY KEY,
    name text NOT NULL
	);    

--Table to storage all matches results
CREATE TABLE IF NOT EXISTS matches(
    winner_ID integer REFERENCES players(player_ID),
    loser_ID integer REFERENCES players(player_ID) CHECK (winner_ID != loser_ID),
    tournament_ID integer REFERENCES tournaments,
    tie boolean, 
	PRIMARY KEY (winner_ID, loser_ID, tournament_ID) or (loser_ID, winer_ID, tournament_ID)
    );    

--Table to storage all the tournaments data
CREATE TABLE IF NOT EXISTS tournaments (
    tournament_ID serial PRIMARY KEY,
    name text NOT NULL
    );


 

