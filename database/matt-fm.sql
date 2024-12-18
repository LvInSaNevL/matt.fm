-- Create the database
CREATE DATABASE mattfm ENCODING 'UTF8';

-- Create roles
CREATE ROLE api_key WITH LOGIN PASSWORD 'Staining4-John-Disallow';
CREATE ROLE dj_matt WITH LOGIN PASSWORD 'Maturely-Unsaid-Barracuda7';

-- Connect to the database
\c mattfm;

-- Grant connect privilege to api_key
GRANT CONNECT ON DATABASE mattfm TO api_key;

-- Create schemas
CREATE SCHEMA reddit;
CREATE SCHEMA youtube;
CREATE SCHEMA mattfm;

-- Create types
CREATE TYPE reddit.subreddits AS ENUM (
  'HeadBangToThis',
  'indiewok',
  'listentothis',
  'musicaljenga',
  'mymusic',
  'newmusic',
  'radioreddit',
  'selfmusic',
  'ThisIsOurMusic',
  'under10k',
  'unheardof'
);

-- Create tables
CREATE TABLE reddit.post (
  subreddit reddit.subreddits,
  date_posted date,
  title varchar(300) NOT NULL,
  permalink varchar(128) PRIMARY KEY,
  upvotes smallint,
  downvotes smallint
);

CREATE TABLE youtube.artists (
  name varchar(100) UNIQUE NOT NULL,
  youtube_id varchar(66) UNIQUE NOT NULL
);

CREATE TABLE youtube.song (
  mattfm_id varchar PRIMARY KEY,
  yt_id varchar(66) UNIQUE NOT NULL,
  published date,
  dates_posted date[],
  genre varchar(64),
  title varchar(100) NOT NULL,
  artist varchar(100) REFERENCES youtube.artists (youtube_id),
  description text NOT NULL,
  viewcount bigint,
  duration int,
  thumbnail varchar(107)
);

CREATE TABLE mattfm.playlist_item (
  date date NOT NULL,
  mattfm_id varchar NOT NULL PRIMARY KEY,
  playlist_id varchar(100) REFERENCES youtube.song (yt_id),
  r_post varchar(128) REFERENCES reddit.post (permalink)
);

-- Grant usage on schema and insert privileges on tables to dj_matt
GRANT USAGE ON SCHEMA mattfm TO dj_matt;
GRANT SELECT, INSERT ON TABLE mattfm.playlist_item TO dj_matt;

GRANT USAGE ON SCHEMA youtube TO dj_matt;
GRANT SELECT, INSERT ON TABLE youtube.song TO dj_matt;
GRANT SELECT, INSERT ON TABLE youtube.artists TO dj_matt;

GRANT USAGE ON SCHEMA reddit TO dj_matt;
GRANT SELECT, INSERT ON TABLE reddit.post TO dj_matt; -- Add this line

-- Grant read-only access for api_key to tables
GRANT USAGE ON SCHEMA mattfm TO api_key;
GRANT SELECT ON TABLE mattfm.playlist_item TO api_key;

GRANT USAGE ON SCHEMA youtube TO api_key;
GRANT SELECT ON TABLE youtube.song TO api_key;
GRANT SELECT ON TABLE youtube.artists TO api_key;

GRANT USAGE ON SCHEMA reddit TO api_key;
GRANT SELECT ON TABLE reddit.post TO api_key;

-- Reload configuration to apply changes
SELECT pg_reload_conf();

-- Double checks that everything worked
\z mattfm.playlist_item;