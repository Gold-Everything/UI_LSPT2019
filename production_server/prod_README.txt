The Dockerfile in this folders creates a container running ubuntu and
installs python, pip, django, nginx, uwsgi

and could be a stand-alone production server for our django project 
however the uwsgi fails, yet reports success in the logs, and i have
yet to pin down the cause of the failure.

contained in this folder are two config files

django - for configuring nginx
django.ini for configuring uwsgi

If/when we just this for production, those two files should be moved to
the same directory as manage.py and the Dockerfile will move them where
they need to go after nginx and uwsgi are installed

NOTE: must change all instance "mysite" to "UI" in Dockerfile before use with 
      official project since this was made around a django prototype.
