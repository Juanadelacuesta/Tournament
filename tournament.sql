-------------------------------------------------------------------------------
-- File: tournament.sql
-- Author: Juana De La Cuesta

-- Table definitions for the tournament project.
-------------------------------------------------------------------------------

-- In order to by able to pair an uneven number of players, the 0 value will
-- be reserved to indicate a player is getting a free win because there is no 
-- opponent available, so the players IDs must start in 0.
CREATE SEQUENCE ID_seq 
  START WITH 1
  INCREMENT BY 1;
 
--Table to storage all players information
CREATE TABLE IF NOT EXISTS players( 
    player_ID  integer DEFAULT nextval('ID_seq') PRIMARY KEY,
    name text NOT NULL
    );    
    
--Table to storage all matches results
CREATE TABLE IF NOT EXISTS matches(
    match_ID serial
    winner_ID integer REFERENCES players(player_ID) NOT NULL,
    loser_ID integer REFERENCES players(player_ID) CHECK (winner_ID != loser_ID),
    tournament_ID integer REFERENCES tournaments,
    tie boolean, 
	PRIMARY KEY (winner_ID, loser_ID, tournament_ID)
    );    


    
--Table to storage all the tournaments data
CREATE TABLE IF NOT EXISTS tournaments (
    tournament_ID serial PRIMARY KEY,
    name text NOT NULL
    );

select winner_ID,count(winner_ID),count(loser_ID) as foo from matches group by winner_ID order by foo desc;



select players.player_ID, players.name, count(winner_ID) as winns from players left join matches on player_ID = winner_ID group by players.player_ID;
select players.player_ID,  count(match_ID) as games from players left join matches on (player_ID = matches.winner_ID OR player_ID = matches.loser_ID) group by player_ID;
 
select name, games.player_ID, games, winns from games, winns where winns.player_ID = games.player_ID order by winns;
