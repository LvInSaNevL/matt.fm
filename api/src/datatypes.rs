use sqlx::FromRow;
use serde::{Serialize, Deserialize};

#[derive(Deserialize, Serialize, FromRow, Debug, Clone)]
pub struct Song {
    pub mattfm_id: String,
    pub yt_id: String,
    pub published: chrono::NaiveDate,
    pub dates_posted: Vec<chrono::NaiveDate>,
    pub genre: Option<String>,
    pub title: String,
    pub artist: Option<String>,
    pub description: String,
    pub viewcount: Option<i64>,
    pub duration: Option<i32>,
    pub thumbnail: Option<String>,
}

#[derive(Deserialize, Serialize, Debug, Clone)]
pub struct Artist {
    pub name: String,
    pub youtube_id: String
}

#[derive(Deserialize, FromRow, Debug, Clone)]
pub struct RedditPost {
    subreddit: String,
    date_posted: String,
    title: String,
    permalink: String,
    upvotes: i16,
    downvotes: i16
}

#[derive(Deserialize, FromRow, Debug, Clone)]
pub struct MfmItem {
    date: String,
    mattfm_id: String,
    playlist_id: String,
    r_post: String
}