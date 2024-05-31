BEGIN;

CREATE DATABASE     MattFm
ENCODING            'UTF8';

\i ../../roles/ApiKey.sql
\i ../../roles/DjMatt.sql

\c MattFm

GRANT           CONNECT
ON DATABASE     MattFm
TO              ApiKey;

\i ../../schemas/dbo.sql

\i ../../tables/Subreddit.sql
\i ../../tables/RedditPost.sql

\i ../../tables/Artist.sql
\i ../../tables/Genre.sql

\i ../../tables/Song.sql
\i ../../tables/SongArtist.sql
\i ../../tables/SongGenre.sql
\i ../../tables/SongPostedOn.sql

\i ../../procedures/sp_CreateArtist.sql
\i ../../procedures/sp_CreateRedditPost.sql

COMMIT;
