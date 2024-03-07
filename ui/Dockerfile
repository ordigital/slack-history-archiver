FROM python:3.11-bookworm

EXPOSE 5001
EXPOSE 5000

# Apt
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y --no-install-recommends \
    nodejs npm

# Python
WORKDIR /app
COPY requirements.txt ./
COPY entrypoint.sh ./
RUN pip install --no-cache-dir -r requirements.txt

# Nodejs
WORKDIR /app/client
COPY ./client/package.json ./
RUN npm install

# Start dev server
WORKDIR /app
CMD [ "bash", "./entrypoint.sh" ]