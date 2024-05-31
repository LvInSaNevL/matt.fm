CREATE PROCEDURE sp_CreateArtist (
    ArtistName  INT,
    YoutubeId   TEXT(66)
)
LANGUAGE SQL
AS $$
    INSERT INTO dbo.Artist
                (YoutubeId, ArtistName)
    VALUES      (YoutubeId, ArtistName);
$$
