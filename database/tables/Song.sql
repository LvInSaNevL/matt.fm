CREATE TABLE dbo.Song (
    SongId              SERIAL      NOT NULL
    PrimaryArtistId     INT         NOT NULL,
    YoutubeId           TEXT(66)    NOT NULL,
    Title               TEXT        NOT NULL,
    [Description]       TEXT        NOT NULL,
    PublishedOn         DATE

    PRIMARY KEY         (SongId),

    FOREIGN KEY         (PrimaryArtistId)
    REFERENCES          dbo.Artist(ArtistId)
)

GRANT       SELECT, INSERT
ON TABLE    dbo.Song
TO          DjMatt;

GRANT       SELECT
ON TABLE    dbo.Song
TO          ApiKey;
