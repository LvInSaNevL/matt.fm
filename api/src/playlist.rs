use crate::datatypes;

use axum::{response::{IntoResponse, Response}, http::StatusCode};
use axum::extract::State;
use sqlx::{postgres::PgPool, Error};
use chrono::Utc;

// SELECT * FROM youtube.song WHERE '2023-12-15'::date=ANY(dates_posted);
pub async fn today(State(pool): State<PgPool>) -> Response {
    let now_date = Utc::now().date_naive();

    // Execute a query
    let query: Result<Vec<datatypes::Song>, Error> = sqlx::query_as::<_, datatypes::Song>(
        "SELECT * FROM youtube.song WHERE $1::date=ANY(dates_posted);"
    ).bind(&now_date)
     .fetch_all(&pool)
     .await;
    
    match query {
        Ok(data) => {
            axum::Json(data).into_response()
        }
        Err(e) => {
            StatusCode::INTERNAL_SERVER_ERROR.into_response()
        }
    }
}