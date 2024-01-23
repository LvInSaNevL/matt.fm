# This is NOT designed to be ran by a person
# This should ONLY be ran during docker build

cd matt-fm/

cargo build --release
cargo run