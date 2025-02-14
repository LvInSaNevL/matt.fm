sudo docker build -t mattfm .
sudo docker run -d --name mattfm mattfm

sudo /bin/bash -c '( echo "30 3    * * *   root    docker run mattfm" >> /etc/crontab )'
sudo /bin/bash -c '( echo "45 3    * * *   root    docker cp mattfm:/mattfm/log.txt $PWD/log.txt" >> /etc/crontab )'