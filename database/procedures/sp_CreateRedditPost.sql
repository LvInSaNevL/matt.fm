CREATE PROCEDURE sp_CreateRedditPost (
    Permalink       TEXT(128),
    SubredditName   TEXT(21),
    SongId          INT,
    Title           TEXT,
    Upvotes         SMALLINT,
    Downvotes       SMALLINT,
)
LANGUAGE SQL
AS $$
    INSERT INTO dbo.RedditPost
            (Permalink, SubredditName,  SongId, Title,  Downvotes,  Upvotes)
    VALUES  (Permalink, SubredditName,  SongId, Title,  Downvotes,  Upvotes)
$$
