use serde::{Serialize, Deserialize};
use axum::extract::State;
use sqlx::{postgres::PgPool, Error, FromRow};

// ######
// Standard data structures
// ######

#[derive(Deserialize, Serialize, FromRow, Debug, Clone)]
pub struct Song {
    pub mattfm_id: String,
    pub yt_id: String,
    pub published: chrono::NaiveDate,
    pub dates_posted: Vec<chrono::NaiveDate>,
    pub genre: String,
    pub title: String,
    pub artist: String,
    pub description: String,
    pub viewcount: i64,
    pub duration: i32,
    pub thumbnail: String,
}
#[derive(Deserialize, Serialize, FromRow, Debug, Clone)]
pub struct MinSong {
    pub yt_id: String,
    pub artist: String,
    pub title: String,
    pub genre: String,
    pub thumbnail: String,
    pub viewcount: i64,
    pub duration: i32
}

#[derive(Deserialize, Serialize, Debug, Clone)]
pub struct Artist {
    pub name: String,
    pub youtube_id: String
}

#[allow(non_camel_case_types)]
#[derive(Deserialize, Serialize, Debug, Clone, sqlx::Type)]
pub enum Subreddits {
    HeadBangToThis,
    indiewok,
    listentothis,
    musicaljenga,
    mymusic,
    newmusic,
    radioreddit,
    selfmusic,
    ThisIsOurMusic,
    under10k,
    unheardof 
}

#[derive(Deserialize, Serialize, FromRow, Debug, Clone)]
pub struct RedditPost {
    pub subreddit: Subreddits,
    pub date_posted: chrono::NaiveDate,
    pub title: String,
    pub permalink: String,
    pub upvotes: i16,
    pub downvotes: i16
}
#[derive(Deserialize, Serialize, FromRow, Debug, Clone)]
pub struct MinReddit {
    pub title: String,
    pub permalink: String
}

#[derive(Deserialize, Serialize, FromRow, Debug)]
pub struct MfmItem {
    pub date: chrono::NaiveDate,
    pub mattfm_id: String,
    pub playlist_id: String,
    pub r_post: String
}
impl Clone for MfmItem {
    fn clone(&self) -> Self {
        MfmItem {
            date: self.date.clone(),
            mattfm_id: self.mattfm_id.clone(),
            playlist_id: self.playlist_id.clone(),
            r_post: self.r_post.clone()
        }
    }
}
#[derive(Deserialize, Serialize, FromRow, Debug, Clone)]
pub struct MinMfmItem {
    pub date: chrono::NaiveDate,
    pub mattfm_id: String
}

// ######
// Return data structures
// ######

#[derive(Deserialize, Serialize, Debug, Clone)]
pub struct FullReturnItem {
    pub mattfm: MinMfmItem,
    pub reddit: RedditPost,
    pub youtube: Song
}
impl FullReturnItem {
    pub async fn New(data: MfmItem, State(pool): State<PgPool>) -> FullReturnItem {
        let r_query: RedditPost = sqlx::query_as::<_, RedditPost>(
            "SELECT * FROM reddit.post WHERE permalink=$1;"
        ).bind(&data.r_post)
         .fetch_one(&pool)
         .await
         .unwrap();

        let y_query: Song = sqlx::query_as::<_, Song>(
            "SELECT * FROM youtube.song WHERE yt_id=$1;"
        ).bind(&data.playlist_id)
         .fetch_one(&pool)
         .await
         .unwrap();

        let mfm_data = MinMfmItem {
            date: data.date,
            mattfm_id: data.mattfm_id
        };

        return FullReturnItem {
            mattfm: mfm_data,
            reddit: r_query,
            youtube: y_query
        }
    }
}
#[derive(Deserialize, Serialize, Debug, Clone)]
pub struct MinReturnItem {
    pub mattfm: MinMfmItem,
    pub reddit: MinReddit,
    pub youtube: MinSong
}
impl MinReturnItem {
    pub async fn New(data: MfmItem, State(pool): State<PgPool>) -> MinReturnItem {
        let r_query: RedditPost = sqlx::query_as::<_, RedditPost>(
            "SELECT * FROM reddit.post WHERE permalink=$1;"
        ).bind(&data.r_post)
         .fetch_one(&pool)
         .await
         .unwrap();
        let r_data = MinReddit {
            title: r_query.title,
            permalink: r_query.permalink
        };

        let y_query: Song = sqlx::query_as::<_, Song>(
            "SELECT * FROM youtube.song WHERE yt_id=$1;"
        ).bind(&data.playlist_id)
         .fetch_one(&pool)
         .await
         .unwrap();
        let y_data = MinSong {
            yt_id: y_query.yt_id,
            artist: y_query.artist,
            title: y_query.title,
            genre: y_query.genre,
            thumbnail: y_query.thumbnail,
            viewcount: y_query.viewcount,
            duration: y_query.duration
        };

        let mfm_data = MinMfmItem {
            date: data.date,
            mattfm_id: data.mattfm_id
        };

        return MinReturnItem {
            mattfm: mfm_data,
            reddit: r_data,
            youtube: y_data
        }
    }
}