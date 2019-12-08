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

#### Install Grafana

1. See official instructions at

> https://grafana.com/docs/grafana/latest/installation/debian/

2. Once installed, start and check that its working with:

> sudo systemctl start grafana-server

> sudo systemctl status grafana-server

#### Install Jmeter

1. First make sure you have Java 8 or higher, check with:
> java -version
2. create directory where you want to install jmeter and go to it
3. download jmeter with:
> wget http://mirror.olnevhost.net/pub/apache//jmeter/binaries/apache-jmeter-5.2.1.tgz
4. unzip with:
> tar -zxvf apache-jmeter-5.2.1.tgz
5. Move to directory:
> ../apache-jmeter-5.2.1/bin
6. Start Jmeter GUI with:
> ./jmeter

### Creating Load Tests with Jmeter GUI

It is easiest to create each test with Jmeter GUI, but recomended to run them in the command line.

#### Creating Basic Load Test .jmx file
1. Move to Directory where jmeter is installed and go to:
> ../apache-jmeter-5.2.1/bin
2. Start Jmeter GUI with:
> ./jmeter
3. Once in GUI, name your test plan
4. right-click current test in left panel and add thread-group
5. Set number of threads and Ramp-up time (add any other properties or extra threads as needed)
6. Make sure Backend Listener is set to send test data to influxdb:
* right-click test in left pannel > add > listener > backend listener
* make sure graphite listener is selected in drop down. Port should match that from what was editted in the influxdb.conf file under graphite
7. Add http request to thread: right-click thread-group in left panel : add > sampler > http request
* set IP, Port, Request type, and Path for request to use for given thread in the test
8. Once youve added all the threads you want, save the test (test will be stored in .jmx file)

(To try out the test within the GUI hit the play button. With Data being streamed to backed, you wont see anything in the GUI but if the server terminal is open, you can see the requests)

### Running Load Tests




