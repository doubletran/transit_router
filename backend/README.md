<div align="center">
  <h1 align="center">AVISSA backend</h1>
  <img src="./documents/static/logo.png" alt="Logo" width="80">
</div>


## Requirements

- Python 3
- PIP
- PostGIS

## Execution

1. Navigate to the repo
```bash
cd backend
```

3. Install the requirement
```console
 pip install Flask

 pip install psycopg

 pip install Flask-Cors

 pip install python-dotenv

 pip install "psycopg[binary]"
```
4. Create the PostgreSQL database in psql
```sql
 create datebase NameOfYourDB;
```
5. Load data import script in psql
``` sql
\i db/create.sql
```
IN PROGRESS

6. Create the .env file and save the following
```html
 DB_HOST=<YourDBConnectionHost>
 DB_PORT=<YourDBConnectionPort>
 DB_NAME=<NameOfYourDB>
 DB_USER=<YourDBConnectionUsername>
 DB_PASSWORD=<YourDBConnectionPassword>
```
7. Run the project
```bash
 python server.py
```
.
