-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- My comments. These database is designed up to 16 players max so max number 
-- of rounds will be 4.
CREATE TABLE player_stats (id serial PRIMARY KEY, name varchar(255), matches int,
wins int, rating float(3));
