-- Create the database if it doesn't exist
CREATE DATABASE "mattfm";

-- Switch to the `mattfm` database
\c mattfm;

CREATE SCHEMA "reddit";

CREATE SCHEMA "lemmy";

CREATE SCHEMA "youtube";

CREATE SCHEMA "social";

CREATE SCHEMA "mattfm";

CREATE TYPE "reddit"."subreddits" AS ENUM (
  'r/HeadBangToThis',
  'r/indiewok',
  'r/listentothis',
  'r/musicaljenga',
  'r/mymusic',
  'r/newmusic',
  'r/radioreddit',
  'r/selfmusic',
  'r/ThisIsOurMusic',
  'r/under10k',
  'r/unheardof'
);

CREATE TABLE "youtube"."song" (
  "yt_id" varchar(66) UNIQUE NOT NULL,
  "published" timestamp,
  "genre" varchar(64),
  "title" varchar(100) NOT NULL,
  "description" TEXT NOT NULL,
  "viewcount" bigint,
  "duration" int,
  "artist" varchar(140),
  "thumbnail" varchar(107)
);

CREATE TABLE "youtube"."artists" (
  "name" varchar(140) PRIMARY KEY,
  "youtube_id" varchar(66) UNIQUE NOT NULL
);

CREATE TABLE "social"."post" (
  "post_id" varchar(300) PRIMARY KEY,
  "platform" TEXT NOT NULL,
  "date_posted" date,
  "author" varchar(40)
);

CREATE TABLE "social"."reddit" (
  "post_id" varchar(300) PRIMARY KEY,
  "title" varchar(300) NOT NULL,
  "subreddit" reddit.subreddits,
  "upvotes" smallint,
  "downvotes" smallint
);

CREATE TABLE "social"."manual" (
  "entry_id" varchar(300) PRIMARY KEY,
  "source" TEXT,
  "permalink" varchar(300),
  "title" varchar(300) NOT NULL
);

CREATE TABLE "mattfm"."playlist" (
  "mattfm_id" varchar(8) PRIMARY KEY NOT NULL
);

CREATE TABLE "mattfm"."playlist_item" (
  "mattfm_id" varchar NOT NULL,
  "song_id" varchar(100) NOT NULL,
  "post_id" varchar(300) NOT NULL,
  "indexed" date,
  "next_play" date,
  "all_plays" date[]
);

ALTER TABLE "youtube"."song" ADD FOREIGN KEY ("artist") REFERENCES "youtube"."artists" ("name");

ALTER TABLE "social"."post" ADD FOREIGN KEY ("post_id") REFERENCES "social"."reddit" ("post_id");

ALTER TABLE "social"."post" ADD FOREIGN KEY ("post_id") REFERENCES "social"."manual" ("entry_id");

ALTER TABLE "mattfm"."playlist_item" ADD FOREIGN KEY ("mattfm_id") REFERENCES "mattfm"."playlist" ("mattfm_id");

ALTER TABLE "mattfm"."playlist_item" ADD FOREIGN KEY ("song_id") REFERENCES "youtube"."song" ("yt_id");

ALTER TABLE "mattfm"."playlist_item" ADD FOREIGN KEY ("post_id") REFERENCES "social"."post" ("post_id");
