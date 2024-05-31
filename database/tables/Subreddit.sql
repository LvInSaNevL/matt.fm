CREATE TABLE dbo.Subreddit (
    SubredditName   TEXT(21)    NOT NULL,
    [Description]   TEXT,

    PRIMARY KEY     (SubredditName)
)

GRANT       SELECT, INSERT
ON TABLE    dbo.Subreddit
TO          DjMatt;

GRANT       SELECT
ON TABLE    dbo.Subreddit
TO          ApiKey;
