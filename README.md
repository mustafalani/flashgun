flashgun
=============

This app provide RESTful API for flashnet https://masstech.com/flashnet/

Key features
------------

 -
 -
 -
 -
 -
 -
 -

Folder Structure
----------------
The following folders must be placed in the root directory of flashgun
```
doc
logs
templates
www
xml
app.py
flashgun.conf
```

Installation
------------
```
sudo apt-get install python-dev

sudo apt-get install python-pip

sudo pip install uwsgi
```

Intsall logviewer websocket
---------------------------
```
cd /opt/flashgun/websocket/logviewer
```

for python
```
sudo pip install -r requirements.txt
```
for python3
```
sudo pip3 install -r requirements.txt
```

for python
```
./ve python server.py --host 127.0.0.1 --port 8864 --prefix /opt/flashgun/playlists/logs/
```

for python3
```
./ve python3 server.py --host 127.0.0.1 --port 8864 --prefix /opt/flashgun/playlists/logs/
```

add flashgun to system services
------------------------------------
```
nano /etc/systemd/system/flashgun.service
```
in the service file write the following:

```
[Unit]
Description=uWSGI instance to serve flashgun
After=network.target

[Service]
WorkingDirectory=/opt/flashgun/
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/flashgun/flask/bin"
ExecStart=/opt/ffplayout/api/flask/bin/uwsgi --ini flashgun.ini
User=root
Group=www-data

[Install]
WantedBy=multi-user.target
```
check the service
----------------------------

```
sudo systemctl daemon-reload

sudo systemctl enable flashgun.service

sudo systemctl start flashgun.service

sudo systemctl status flashgun.service
```

add logviewer websocket to system services
------------------------------------------
```
nano /etc/systemd/system/flashgun-websocket.service
```
in the service file write the following:

```
[Unit]
Description=websocket instance to serve flashgun
After=network.target

[Service]
WorkingDirectory=/opt/flashgun/websocket/logviewer/
Environment="PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/flashgun/flask/bin"
ExecStart=/opt/flashgun/websocket/logviewer/ve python3 server.py --host 127.0.0.1 --port 8864 --prefix /opt/flashgun/logs/
User=root
Group=www-data

[Install]
WantedBy=multi-user.target
```

check the service
----------------------------

```
sudo systemctl daemon-reload

sudo systemctl enable flashgun-websocket.service

sudo systemctl start flashgun-websocket.service

sudo systemctl status flashgun-websocket.service
```

configure nginx
----------------------------
sudo mkdir /var/www/flashgun

sudo nano /var/www/flashgun/http.conf


```
server {
    listen 8085;
    server_name localhost;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/opt/flashgun/flashgun.sock;
    }
}
server {
    listen                      8865 ssl;
    listen                      [::]:8865 ssl;

    ssl_certificate             /etc/letsencrypt/live/ott-pl-02.iohub.live/fullchain.pem;
    ssl_certificate_key         /etc/letsencrypt/live/ott-pl-02.iohub.live/privkey.pem;
    ssl_trusted_certificate     /etc/letsencrypt/live/ott-pl-02.iohub.live/chain.pem;

    location / {
      proxy_pass  http://127.0.0.1:8864;
      proxy_http_version 1.1;
      proxy_set_header Upgrade $http_upgrade;
      proxy_set_header Connection "upgrade";

         }
}
```
