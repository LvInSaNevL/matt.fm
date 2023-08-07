CREATE DATABASE mattfm ENCODING 'UTF8';

\c mattfm

CREATE SCHEMA reddit;
CREATE SCHEMA youtube;
CREATE SCHEMA mattfm;

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
  genre varchar(64),
  title varchar(100) NOT NULL,
  artist varchar(100) REFERENCES youtube.artists (name),
  description text NOT NULL,
  viewcount bigint,
  duration int,
  thumbnail varchar(107)
);

CREATE TABLE mattfm.playlist_item (
  date date NOT NULL,
  mattfm_id varchar REFERENCES youtube.song (mattfm_id),
  playlist_id varchar(100) NOT NULL,
  r_post varchar(128) REFERENCES reddit.post (permalink)
);
