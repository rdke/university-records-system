# University Records System

A Django starter project for managing university records.

## Setup

```bash
brew install mysql-client pkg-config
export PKG_CONFIG_PATH="$(brew --prefix mysql-client)/lib/pkgconfig"
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

In MySQL Workbench, run:

```sql
CREATE DATABASE university_records CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'university_records'@'localhost' IDENTIFIED BY 'your-password';
GRANT ALL PRIVILEGES ON university_records.* TO 'university_records'@'localhost';
```

Copy `.env.example` to `.env` and add the same password:

```bash
cp .env.example .env
```

Then run:

```bash
python manage.py migrate
python manage.py runserver
```

Open `http://127.0.0.1:8000/`.