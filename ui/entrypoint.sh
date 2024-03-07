#!/bin/bash
cd /app/flask && flask run --port=5001 --host=0.0.0.0 --debug & cd /app/client && npm run dev
