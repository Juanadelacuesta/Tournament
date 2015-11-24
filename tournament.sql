-------------------------------------------------------------------------------
-- File: tournament.sql
-- Author: Juana De La Cuesta

-- Table definitions for the tournament project.
-------------------------------------------------------------------------------

--Table to storage all players information
CREATE TABLE IF NOT EXISTS players (
    player_ID serial PRIMARY KEY,
    name text CHECK NOT NULL
	);    

--Table to storage all matches results
CREATE TABLE IF NOT EXISTS matches(
    player1_ID integer REFERENCES players(player_ID),
    player2_ID integer REFERENCES players(player_ID),
    tournament_ID integer REFERENCES tournaments,
    results integer NOT NULL,
	PRIMARY KEY (player1_ID, player2_ID, tournament_ID)
    );    

--Table to storage all the tournaments data
CREATE TABLE IF NOT EXISTS tournaments (
    tournament_ID serial PRIMARY KEY,
    name text NOT NULL
    );



