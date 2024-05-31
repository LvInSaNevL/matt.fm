mod config;
mod data;
mod datatypes;
mod domain;
mod playlist;
mod routes;
mod song;
mod state;

use axum::{
    response::Html,
    routing::{get, post},
    Router,
};
use config::AppConfig;
use routes::*;
use sqlx::postgres::PgPoolOptions;
use state::AppState;
use std::{env, io};
use tokio::net::TcpListener;

#[derive(thiserror::Error, Debug)]
enum Error {
    #[error("Failed to load environment file: {0}")]
    FailedToLoadEnvironmentFile(#[from] dotenvy::Error),

    #[error("Failed to load app config: {0}")]
    FailedToLoadAppConfig(#[from] config::Error),

    #[error("Failed to acquire database connection: {0}")]
    FailedToAcquireDatabaseConnection(#[from] sqlx::Error),

    #[error("Failed to initialize TCP listener: {0}")]
    FailedToInitializeListener(io::Error),

    #[error("Failed to serve Axum router: {0}")]
    FailedToServeAxumRouter(io::Error),
}

#[tokio::main]
async fn main() -> Result<(), Error> {
    // Loads env file
    dotenvy::dotenv()?;

    let config = AppConfig::load_env()?;

    for (key, value) in env::vars() {
        println!("{key}: {value}");
    }

    // Connects to the DB
    let pool = PgPoolOptions::new()
        .max_connections(config.database_max_connections)
        .acquire_timeout(config.database_timeout)
        .connect(&config.database_url)
        .await?;

    // build our application with a route
    let app = Router::new()
        .route("/", get(handler))
        .route("/song/full", post(song::full))
        .route("/song/minimal", post(song::minimal))
        .route("/playlist/today", get(playlist::today))
        .nest("/heartbeat", heartbeat::router())
        .with_state(AppState::new(pool));

    // run it
    let listener = TcpListener::bind("0.0.0.0:6676")
        .await
        .map_err(|e| Error::FailedToInitializeListener(e))?;

    println!("listening on {}", listener.local_addr().unwrap());

    axum::serve(listener, app)
        .await
        .map_err(|e| Error::FailedToServeAxumRouter(e))
}

// Catch all function for fake URLs
pub async fn handler() -> Html<&'static str> {
    Html("<h1>Hey! You weren't supposed to see this!</h1>")
}
