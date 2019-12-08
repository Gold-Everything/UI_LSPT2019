# UI_LSPT2019   

## Instructions for Starting Server in VM

1. Be on RPI network, get login credentials from email
2. Use putty or in linux terminal type:
> ssh \<username\>@lspt-query2.cs.rpi.edu
3. Once in VM navigate to current repo: 
> cd /home/gibboa/ui_query/UI_LSPT2019/
4. To start server use:
> python3 manage.py runserver 0.0.0.0:8080
5. Test in browser using: 
> http://lspt-query2.cs.rpi.edu:8080/

## Instructions for Running Performance/Load Tests

### Installation

load test uses jmeter and will pass test data to Grafana gui via a simple InfluxDB setup

#### Install InfluxDB (Linux)

1. 
