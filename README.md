# Lab Inventory

A Django inventory app for tracking products, stock adjustments, and change history.

## Run locally on Windows

Use Python 3.12 or newer. From the repository folder, create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Run database migrations and start the development server:

```powershell
$env:DJANGO_DEBUG = "true"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open <http://127.0.0.1:8000/> and sign in. Product registration and deletion are restricted to the superuser. The SQLite database is stored in `db.sqlite3`; back it up before moving or replacing it. Product CSV import/export is available in Django Admin.

## Deployment configuration

Set `DJANGO_DEBUG=false`, `DJANGO_SECRET_KEY` to a private random value, and `DJANGO_ALLOWED_HOSTS` to a comma-separated list of the app's hostnames. Set `DATABASE_URL` to a persistent PostgreSQL database URL for hosted use; without it the app uses local SQLite. Serve the app through the provided Gunicorn `Procfile`, enable HTTPS, and run `python manage.py check --deploy` with the production environment before deploying.

## Inventory behavior

- Signed-in users can view products, make stock adjustments, and review the change history.
- Only a superuser can add or delete products.
- Stock adjustments are recorded with the user and timestamp, and quantities cannot become negative or exceed 32,767 units.

## Credits

The original stock-management template was based on [Leonardo de Souza's project](https://github.com/Leonardo8133/stock_manage).
