### Convert sass/scss in css

for this we can use many sass/scss compiler but here we gona use Vscode live sass compiler
step 1: Download the live sass compiler extension in vscode
step 2: pest the script billow in settings.json

"liveSassCompile.settings.formats": [
{
"format": "expanded",
"extensionName": ".css",
"savePath": "~/../css"
}
]

## To delete the migration files

#### `find . -path "*/migrations/*.py" -not -name "__init__.py" -delete`

#### `find . -path "*/*.pyc" -delete`

#### `rm -f db.sqlite3`

#### `find . -path "*/__pycache__" -delete`