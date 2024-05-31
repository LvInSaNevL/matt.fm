use axum::extract::FromRef;
use sqlx::PgPool;

use crate::state::AppState;

pub struct SongRepository {
    pool: PgPool,
}

impl FromRef<AppState> for SongRepository {
    fn from_ref(input: &AppState) -> Self {
        Self {
            pool: input.pool.clone(),
        }
    }
}
