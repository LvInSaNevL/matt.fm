sudo docker kill mattfm_sql mattfm_sql_admin
sudo docker rm mattfm_sql mattfm_sql_admin
sudo docker network prune

sudo docker compose up --no-recreate