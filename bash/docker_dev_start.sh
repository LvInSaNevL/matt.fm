sudo docker kill mattfm_proxy mattfm_sql mattfm_sql_admin mattfm_api
sudo docker rm mattfm_proxy mattfm_sql mattfm_sql_admin mattfm_api
sudo docker network prune

sudo docker compose up --no-recreate