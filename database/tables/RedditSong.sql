CREATE TABLE dbo.RedditPost (
    Permalink       TEXT(128)   NOT NULL,
    SubredditName   TEXT(21)    NOT NULL,
    SongId          INT         NOT NULL,
    Title           TEXT        NOT NULL,
    PostedOn        DATE        DEFAULT CURRENT_TIMESTAMP,
    Upvotes         SMALLINT    DEFAULT 0,
    Downvotes       SMALLINT    DEFAULT 0,

    PRIMARY KEY     (Permalink)

    FOREIGN KEY     (SubredditName)
    REFERENCES      dbo.Subreddit(SubredditName),

    FOREIGN KEY     (SongId)
    REFERENCES      dbo.Song(SongId)
)

GRANT       SELECT, INSERT
ON TABLE    dbo.RedditPost
TO          DjMatt;

GRANT       SELECT
ON TABLE    dbo.RedditPost
TO          ApiKey;
