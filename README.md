## To delete the migration files

### `$ find . -path "*/migrations/*.py" -not -name "__init__.py" -delete`

### `$ find . -path "*/migrations/*.pyc" -delete`

### `$ rm -f db.sqlite3`
