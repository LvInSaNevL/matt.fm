CREATE TABLE dbo.Artist (
    ArtistId        SERIAL      NOT NULL,
    ArtistName      TEXT        NOT NULL,

    PRIMARY KEY     (ArtistId)
)

GRANT       SELECT, INSERT
ON TABLE    dbo.Artist
TO          DjMatt;

GRANT       SELECT
ON TABLE    dbo.Artist
TO          ApiKey;
