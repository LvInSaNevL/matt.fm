pub mod heartbeat;
pub mod song;

mod prelude {
    pub use crate::state::AppState;

    pub use axum::http::StatusCode;
    pub use axum::response::IntoResponse;
    pub use axum::routing::get;
    pub use axum::Router;
}
