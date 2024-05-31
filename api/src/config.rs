use std::{
    env::{self, VarError},
    num::ParseIntError,
    time::Duration,
};

#[derive(thiserror::Error, Debug)]
pub enum Error {
    #[error("Failed to load environment variable: {0}")]
    FailedToLoadEnvironmentVariable(#[from] VarError),

    #[error("Could not parse environment variable: {0}")]
    CouldNotParseEnvironmentVariable(#[from] ParseIntError),
}

#[derive(Debug)]
pub struct AppConfig {
    pub database_max_connections: u32,
    pub database_timeout: Duration,
    pub database_url: String,
    pub app_url: String,
}

impl AppConfig {
    pub fn load_env() -> Result<Self, Error> {
        Ok(Self {
            database_max_connections: "DATABASE_MAX_CONNECTIONS".try_get()?,
            database_timeout: "DATABASE_TIMEOUT_MS".try_get()?,
            database_url: "DATABASE_URL".try_get()?,
            app_url: "APP_URL".try_get()?,
        })
    }
}

trait FromEnv<T> {
    fn try_get(self) -> Result<T, Error>;
}

impl<'a> FromEnv<String> for &'a str {
    fn try_get(self) -> Result<String, Error> {
        Ok(env::var(self)?)
    }
}

impl<'a> FromEnv<u32> for &'a str {
    fn try_get(self) -> Result<u32, Error> {
        Ok(env::var(self)?.parse::<u32>()?)
    }
}

impl<'a> FromEnv<Duration> for &'a str {
    fn try_get(self) -> Result<Duration, Error> {
        Ok(env::var(self)?.parse::<u64>().map(Duration::from_millis)?)
    }
}
