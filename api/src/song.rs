use crate::datatypes;

use serde::Deserialize;
use axum::{response::{IntoResponse, Response}, http::StatusCode};
use axum::extract::{State, Json};
use sqlx::{PgPool, Error};

#[derive(Deserialize, Debug)]
pub struct SongRequest { pub mfm_id: Vec<String> }

// SELECT * FROM youtube.song WHERE mattfm_id='%id%';
pub async fn full(State(pool): State<PgPool>, Json(payload): Json<SongRequest>) -> Response {
    let mut response: Vec<datatypes::Song> = Vec::new();

    for song in payload.mfm_id.into_iter() {
        let query: Result<datatypes::Song, Error> = sqlx::query_as::<_, datatypes::Song>(
            "SELECT * FROM youtube.song WHERE mattfm_id=$1;"
        ).bind(&song)
         .fetch_one(&pool)
         .await;
        
        match query {
            Ok(data) => {
                response.push(data)
            }
            Err(e) => {
                return StatusCode::INTERNAL_SERVER_ERROR.into_response()
            }
        }
    }

    axum::Json(response).into_response()
}