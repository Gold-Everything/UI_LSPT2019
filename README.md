# UI_LSPT2019   

## Instructions for Starting Server in VM

1. Be on RPI network, get login credentials from email
2. Use putty or in linux terminal type:
> ssh \<username\>@lspt-query2.cs.rpi.edu
3. Once in VM, navigate to current repo: 
> cd /home/gibboa/ui_query/UI_LSPT2019/
4. To start server use:
> python3 manage.py runserver 0.0.0.0:8080
5. Test in browser using: 
> http://lspt-query2.cs.rpi.edu:8080/

## Instructions for Running Performance/Load Tests

### Installation

load test uses jmeter and will pass test data to Grafana GUI via a simple InfluxDB setup

#### Install InfluxDB (Linux- Debian/Ubuntu)

1. Download or use
> wget https://dl.influxdata.com/influxdb/releases/influxdb_1.7.9_amd64.deb

> sudo dpkg -i influxdb_1.7.9_amd64.deb
2. Test server with 
> sudo influxd
(to avoid sudo must change permissions to allow influx db to do 'mkdir /var/lib/influxdb/meta')
3. You must enable graphite endpoint for influxdb. Go to influxdb.conf at the path:
> /etc/influxdb/influxdb.conf

(make sure you have permission ot edit file - sudo vim - is easiest)
above and uncomment and alter the following lines to match:

> [[graphite]]

> enabled = true

> database = "jmeter"

> retention-policy = ""

> bind-address = ":2003"

> protocol = "tcp"

> consistency-level = "one"

> batch-size = 5000

> batch-pending = 10

> batch-timeout = "1s" 

> udp-read-buffer = 0

4. Finally we need go into influx db and make a database named 'jmeter'

* In one terminal, to start database, type:

> influxd 

(Note, check the text in the terminal as the database starts for a line that mentions "starting graphite service" to ensure that it was successfully enabled)

* In a second terminal access te database with:

> influx

* Once inside the database in the second terminal type:

> CREATE DATABASE jmeter

(SHOW DATABASES to check existing databases)

* exit influx db with

> exit

