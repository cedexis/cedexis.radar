docker-up-ubuntu-10.04:
	sudo docker build -t cedexis.radar-ubuntu-10.04 docker/ubuntu-10.04/

docker-run-ubuntu-10.04:
	sudo docker run -t cedexis.radar-ubuntu-10.04 cedexis-radar-cli -c 11475
