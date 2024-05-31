CREATE TABLE dbo.SongGenre (
    SongId          INT,
    Genre           TEXT(64),

    PRIMARY KEY     (SongId, Genre),

    FOREIGN KEY     (SongId)
    REFERENCES      dbo.Song(SongId),

    FOREIGN KEY     (Genre)
    REFERENCES      dbo.Genre([Description])
)

GRANT       SELECT, INSERT
ON TABLE    dbo.SongGenre
TO          DjMatt;

GRANT       SELECT
ON TABLE    dbo.SongGenre
TO          ApiKey;
