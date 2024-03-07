# Slack History Archiver (aka Slackadoodoo)

![slack history archiver ui](https://i.ibb.co/Rvhgdzg/slack.jpg)

This project allows you to download available message history from Slack server. History is limited in free accounts so this way you can keep private archive of messages by running script everyday via cron. To make it work you need only a website token and a cookie. There is also a simple UI based on Flask and Vue.

** Use at your own risk. I do not take any legal responsibility for data processed by this scripts. This is only a data collection tool for private use. **

### 1. Download:

```bash
$ git clone git@github.com:ordigital/slack-history-archiver.git
```

### 2. Edit `config.yaml` and put your token and cookie. Instructions for Chrome based browser:

1. Open slack server in browser, for ex. https://YOURSERVER.slack.com
2. Go to Dev Tools (F12) → Network. Refresh page and search for `info`. Queries with `info?p=48` or similar should appear. Click on it with left mouse button.
3. Open Payload tab on right, copy `token` content and paste it as a value of `token` in `config.yaml` file.
4. Right mouse button click on `info?p=48` and select `copy`→ `copy as cURL`.
5. Paste clipboard contents to text editor and copy `cookie` header content (without quotation marks) to `cookie` field in `config.yaml`
6. Put yout server address (for ex. `https://YOURSERVER.slack.com`) to `server` field in `config.yaml`

### 3. Install requirements:

(You can also create `venv` or find required packages in `apt` or your OS package manager)

```
$ pip install -r requirements.txt
```

### 4. Start fetching:

First run will take some time cause it tries to fetch messages from last 3 months. Next runs will fetch only last messages by checking timestamp so it will be faster.

```
$ python ./slackadoodoo.py
```

### 5. Run UI using Docker:

Running script bellow will build and run docker image with dev environment containing Flask backend and Vue frontend. It will copy database at run and not use the original file. 

```
./start-ui.sh
```
UI is intended for local and private use only because of security and legal reasons.
```
Vue client address is: http://localhost:5000 
Flask api: https://localhost:5001
```



