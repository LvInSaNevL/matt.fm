CREATE TABLE dbo.Genre (
    [Description]   TEXT(64),

    PRIMARY KEY     ([Description])
)

GRANT       SELECT, INSERT
ON TABLE    dbo.Genre
TO          DjMatt;

GRANT       SELECT
ON TABLE    dbo.Genre
TO          ApiKey;
