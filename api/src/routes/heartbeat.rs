use super::prelude::*;

pub fn router() -> Router<AppState> {
    Router::new().route("/", get(heartbeat))
}

async fn heartbeat() -> impl IntoResponse {
    StatusCode::OK
}
