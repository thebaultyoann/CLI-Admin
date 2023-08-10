#!/bin/bash
sudo docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mariadb > ~/CLI-Admin-test/mariadb_ip
