# Deploying the application

1. SSH into the application server.
2. Perform a database backup:
  1. `sudo su - postgres`
  2. `pg_dump watersharingdb > ~/watersharingdb_<date>.sql`
  3. `exit`
3. Change to the superuser: `sudo su`
4. Change to the web application directory: `cd /var/www/watersharingdashboard`
5. Load the Django environment: `source scripts/deployment.sh`
6. Stop Apache: `service apache2 stop`
7. Get the latest version of the waterkit repository: `pushd /path/to/waterkit && git pull`.
8. Update waterkit: `pip uninstall waterkit && python setup.py install`
9. Go back to the web application directory: `popd`
10. Update the application code: `git pull`
11. Update the requirements: `pip install -r requirements.txt`
11. Update the database: `python manage.py migrate`
12. Update the static files: `python manage.py collectstatic`
13. Start apache: `service apache2 start`
