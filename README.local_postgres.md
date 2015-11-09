Using Local Postgres
====================

1. Obtain a production database backup.
2. createuser watersharinguser
2. dropdb watersharingdb
3. createdb -T template0 watersharingdb
4. psql watersharingdb < /path/to/backup/file
5. rsync -avz productionserver:/path/to/watersharingdashboard/media .
