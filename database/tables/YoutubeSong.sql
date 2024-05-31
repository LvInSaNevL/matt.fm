CREATE TABLE dbo.YoutubeSong (
    SongId          INT         NOT NULL,
    YoutubeId       TEXT(66)    NOT NULL,

    PRIMARY KEY     (SongId),

    FOREIGN KEY     (SongId)
    REFERENCES      dbo.Song(SongId)
)

GRANT       SELECT, INSERT
ON TABLE    dbo.YoutubeSong
TO          DjMatt;

GRANT       SELECT
ON TABLE    dbo.YoutubeSong
TO          ApiKey;
