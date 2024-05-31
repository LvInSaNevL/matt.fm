IF NOT EXISTS ( SELECT      1
                FROM        dbo.Subreddit)
THEN

    INSERT INTO dbo.Subreddit
            (SubredditName)
    VALUES  ("HeadBangToThis"   ),
            ("indiewok"         ),
            ("listentothis"     ),
            ("musicaljenga"     ),
            ("mymusic"          ),
            ("newmusic"         ),
            ("radioreddit"      ),
            ("selfmusic"        ),
            ("ThisIsOurMusic"   ),
            ("under10k"         ),
            ("unheardof"        );

END IF;
