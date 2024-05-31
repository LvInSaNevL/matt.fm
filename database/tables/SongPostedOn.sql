CREATE TABLE dbo.SongPostedOn (
    SongId          INT     NOT NULL,
    PostedOn        DATE    NOT NULL,

    PRIMARY KEY     (SongId, PostedOn),

    FOREIGN KEY     (SongId)
    REFERENCES      dbo.Song(SongId),
)

GRANT       SELECT, INSERT
ON TABLE    dbo.SongPostedOn
TO          DjMatt;

GRANT       SELECT
ON TABLE    dbo.SongPostedOn
TO          ApiKey;
