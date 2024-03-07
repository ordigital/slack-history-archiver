#!/bin/bash
cp ./data/slack.sqlite ./ui/flask/db.sqlite
cd ui
docker-compose up --build app

