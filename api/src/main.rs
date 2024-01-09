mod playlist;
mod datatypes;
mod song;

use axum::{
    response::Html,
    routing::{get, post},
    Router,
};
use sqlx::postgres::PgPoolOptions;
use std::time::Duration;
use dotenvy::dotenv;
use std::env;

#[tokio::main]
async fn main() {
    // Loads env file
    dotenv().ok();
    for (key, value) in env::vars() {
        println!("{key}: {value}");
    };

    // Connects to the DB
    let pool = PgPoolOptions::new()
        .max_connections(5)
        .acquire_timeout(Duration::from_secs(3))
        .connect(&env::var("DB_URL").unwrap())
        .await
        .expect("can't connect to database");

    // build our application with a route
    let app = Router::new().route("/", get(handler))
                           .route("/song/full", post(song::full))
                           .route("/playlist/today", get(playlist::today))
                           .with_state(pool);

    // run it
    let listener = tokio::net::TcpListener::bind("127.0.0.1:6676")
        .await
        .unwrap();
    println!("listening on {}", listener.local_addr().unwrap());
    axum::serve(listener, app).await.unwrap();
}

// Catch all function for fake URLs
pub async fn handler() -> Html<&'static str> {
    Html("<h1>Hey! You weren't supposed to see this!</h1>")
}