CREATE TABLE dbo.SongArtist (
    SongId          INT,
    ArtistId        INT,

    PRIMARY KEY     (SongId, ArtistId),

    FOREIGN KEY     (SongId)
    REFERENCES      dbo.Song(SongId),

    FOREIGN KEY     (ArtistId)
    REFERENCES      dbo.Artist(ArtistId)
)

GRANT       SELECT, INSERT
ON TABLE    dbo.SongArtist
TO          DjMatt;

GRANT       SELECT
ON TABLE    dbo.SongArtist
TO          ApiKey;
