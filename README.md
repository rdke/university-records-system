# University Records System

A Django starter project for managing university records.

## Setup

### Windows
```sh
winget install --source winget --exact --id Python.Python.3.14
winget install --source winget --exact --id Oracle.MySQL --version 8.4.9
Set-Alias python "$env:LOCALAPPDATA\Programs\Python\Python314\python.exe"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### MacOS
```bash
brew install python@3.14 mysql@8.4 pkg-config
brew services start mysql@8.4
export PKG_CONFIG_PATH="$(brew --prefix mysql@8.4)/lib/pkgconfig"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

In MySQL Workbench, run:

```sql
CREATE DATABASE university_records;
CREATE USER 'university_records'@'localhost' IDENTIFIED BY 'your-password';
GRANT ALL PRIVILEGES ON university_records.* TO 'university_records'@'localhost';
```

Copy `.env.example` to `.env` and set the credentials, host and port of the MySQL server inside the file:

```bash
cp .env.example .env
```

Then run:

```bash
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

And open `http://127.0.0.1:8000/`.

## Database design script

`university.sql` provides the schema, the application creates and populates the database independently.

To import the database:
```bash
mysql -u root -p < university_db.sql
```