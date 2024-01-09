use crate::datatypes;

use axum::{response::{IntoResponse, Response}, http::StatusCode};
use axum::extract::State;
use sqlx::{postgres::PgPool, Error};
use chrono::Utc;

// SELECT * FROM youtube.song WHERE '%date%'::date=ANY(dates_posted);
pub async fn today(State(pool): State<PgPool>) -> Response {
    let now_date = Utc::now().date_naive();

    // Execute a query
    let query: Result<Vec<datatypes::MfmItem>, Error> = sqlx::query_as::<_, datatypes::MfmItem>(
        "SELECT * FROM mattfm.playlist_item WHERE date=$1;"
    ).bind(&now_date)
     .fetch_all(&pool)
     .await;
    
    match query {
        Ok(data) => {
            let mut return_songs: Vec<datatypes::MinReturnItem> = Vec::new();
            for song in data.iter() {
                return_songs.push(datatypes::MinReturnItem::New(song.clone(), axum::extract::State(pool.clone())).await);
            }
            if return_songs.is_empty() { return StatusCode::NO_CONTENT.into_response() }
            else { axum::Json(return_songs).into_response() }
        }
        Err(e) => {
            StatusCode::INTERNAL_SERVER_ERROR.into_response()
        }
    }
}