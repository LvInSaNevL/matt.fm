use crate::datatypes;

use serde::Deserialize;
use axum::{response::{IntoResponse, Response}, http::StatusCode};
use axum::extract::{State, Json};
use sqlx::{PgPool, Error};

#[derive(Deserialize, Debug)]
pub struct SongRequest { pub mfm_id: Vec<String> }

// SELECT * FROM youtube.song WHERE mattfm_id='%id%';
pub async fn full(State(pool): State<PgPool>, Json(payload): Json<SongRequest>) -> Response {
    let mut response: Vec<datatypes::FullReturnItem> = Vec::new();

    for song in payload.mfm_id.into_iter() {
        let query: Result<datatypes::MfmItem, Error> = sqlx::query_as::<_, datatypes::MfmItem>(
            "SELECT * FROM mattfm.playlist_item WHERE mattfm_id=$1;"
        ).bind(&song)
         .fetch_one(&pool)
         .await;
        
        match query {
            Ok(data) => {
                response.push(datatypes::FullReturnItem::new(data.clone(), axum::extract::State(pool.clone())).await);
            }
            Err(e) => {
                return StatusCode::INTERNAL_SERVER_ERROR.into_response()
            }
        }
    }
    if response.is_empty() { return StatusCode::NO_CONTENT.into_response() }
    else { return axum::Json(response).into_response() }
}

pub async fn minimal(State(pool): State<PgPool>, Json(payload): Json<SongRequest>) -> Response {
    let mut response: Vec<datatypes::MinReturnItem> = Vec::new();

    for song in payload.mfm_id.into_iter() {
        let query: Result<datatypes::MfmItem, Error> = sqlx::query_as::<_, datatypes::MfmItem>(
            "SELECT * FROM mattfm.playlist_item WHERE mattfm_id=$1;"
        ).bind(&song)
         .fetch_one(&pool)
         .await;
        
        match query {
            Ok(data) => {
                response.push(datatypes::MinReturnItem::new(data.clone(), axum::extract::State(pool.clone())).await);
            }
            Err(e) => {
                return StatusCode::INTERNAL_SERVER_ERROR.into_response()
            }
        }
    }

    axum::Json(response).into_response()
}