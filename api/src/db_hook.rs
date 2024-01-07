use tokio_postgres::{Client, Socket, NoTls, Error};

const DB_URL: &str = "postgres://postgres:postgres@localhost:5432/postgres";

pub async fn db_connect() -> (Client, tokio_postgres::Connection<Socket, NoTlsStream>) {
    let (client, connection) = tokio_postgres::connect(
        "postgres://postgres:postgres@localhost:5432/postgres",
        NoTls,
      )
      .await

    tokio::spawn(async move {
        if let Err(error) = connection.await {
          eprintln!("Connection error: {}", error);
        }
      });

    return client;
}