CREATE TABLE dbo.YoutubeArtist (
    ArtistId        INT         NOT NULL,
    YoutubeId       TEXT(66)    NOT NULL,

    PRIMARY KEY     (ArtistId),

    FOREIGN KEY     (ArtistId)
    REFERENCES      dbo.Artist(ArtistId)
)

GRANT       SELECT, INSERT
ON TABLE    dbo.YoutubeArtist
TO          DjMatt;

GRANT       SELECT
ON TABLE    dbo.YoutubeArtist
TO          ApiKey;
