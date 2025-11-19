# Guia de Configuració de Linting i Format Automàtic

Aquest projecte té configurades eines de linting i format automàtic per mantenir la qualitat del codi.

## 🎯 Eines Configurades

- **black** - Format automàtic de codi Python
- **isort** - Ordenació automàtica d'imports
- **flake8** - Linter per detectar errors i estil
- **mypy** - Type checker estàtic
- **bandit** - Analitzador de seguretat
- **pre-commit** - Execució automàtica en cada commit

## 🚀 Configuració Inicial

### 1. Instal·lar pre-commit hooks

```bash
./setup_dev.sh
```

O manualment:

```bash
pip install pre-commit
make install-hooks
```

Això instal·larà els git hooks que s'executaran automàticament abans de cada commit.

### 2. Aplicar format a tot el repositori (primera vegada)

```bash
./format_all.sh
```

O amb make:

```bash
make format
```

## 📝 Comandes Disponibles

### Format del codi

```bash
# Formatar tot el codi (black + isort)
make format

# Només black
black .

# Només isort
isort .
```

### Linting (comprovació sense canvis)

```bash
# Executar tots els linters
make lint

# Només flake8
flake8 .

# Només mypy (type checking)
make typecheck
# o
mypy .
```

### Security checks

```bash
# Executar checks de seguretat
make security-check

# Només bandit
bandit -r . -c pyproject.toml

# Django security check
make check-security
# o
python manage.py check --deploy
```

### Tests

```bash
# Executar tots els tests
make test

# Tests amb coverage
make coverage

# Tests específics
make test-unit
make test-integration
make test-security
```

### Pre-commit

```bash
# Executar pre-commit en tots els fitxers
make pre-commit-all

# Actualitzar versions dels hooks
make update-hooks
```

### Neteja

```bash
# Netejar fitxers temporals
make clean
```

## 🎨 Format Automàtic on Save (VS Code)

Si utilitzeu VS Code, ja està configurat per formatar automàticament quan deseu:

1. Assegureu-vos que teniu instal·lades les extensions:
   - Python (Microsoft)
   - Black Formatter
   - isort

2. El fitxer `.vscode/settings.json` ja configura:
   - Format on save ✅
   - Black com a formatter ✅
   - isort per imports ✅
   - Flake8 com a linter ✅

## ⚙️ Configuració per Altres Editors

### PyCharm / IntelliJ IDEA

1. **Black:**
   - Settings → Tools → File Watchers
   - Add → black
   - Arguments: `$FilePath$`

2. **isort:**
   - Settings → Tools → File Watchers
   - Add → isort
   - Arguments: `$FilePath$`

3. **Flake8:**
   - Settings → Editor → Inspections
   - Enable Flake8

### Vim/Neovim

Afegir a `.vimrc` o `init.vim`:

```vim
" Black
autocmd BufWritePre *.py execute ':Black'

" isort
autocmd BufWritePre *.py execute ':Isort'
```

### Sublime Text

Instal·lar paquets:
- Python Black
- isort
- SublimeLinter
- SublimeLinter-flake8

### EditorConfig

Tots els editors que suporten EditorConfig llegiran automàticament `.editorconfig` per:
- Indentació (4 espais per Python)
- Final de línia (LF)
- Charset (UTF-8)
- Línia final buida

## 🔄 Workflow de Desenvolupament

### 1. Abans de començar a treballar

```bash
git pull
make clean
```

### 2. Durant el desenvolupament

El format es pot aplicar automàticament:
- **VS Code:** Al desar (Ctrl+S / Cmd+S)
- **Manual:** `make format`

### 3. Abans de fer commit

Pre-commit s'executa automàticament, però pots executar-lo manualment:

```bash
make pre-commit-all
```

### 4. Si pre-commit falla

Pre-commit pot fer canvis automàtics (format). Si això passa:

```bash
git add .
git commit -m "Your message"
```

### 5. Abans de fer push

```bash
# Executar tots els checks
make check

# O individualment
make lint
make security-check
make test
```

## 📋 Configuració del Projecte

### pyproject.toml

Conté la configuració de totes les eines:

```toml
[tool.black]
line-length = 120
target-version = ['py312']

[tool.isort]
profile = "black"
line_length = 120

[tool.mypy]
python_version = "3.12"
warn_return_any = true

[tool.bandit]
exclude_dirs = ["tests", "migrations", ".venv"]
```

### .pre-commit-config.yaml

Defineix els hooks que s'executaran:

- trailing-whitespace
- end-of-file-fixer
- check-yaml, check-json
- black, isort, flake8
- bandit, mypy

## 🐛 Resolució de Problemes

### Pre-commit no s'executa

```bash
# Reinstal·lar hooks
pre-commit uninstall
make install-hooks
```

### Black/isort no funcionen a VS Code

```bash
# Verificar que estan instal·lats
pip list | grep black
pip list | grep isort

# Reinstal·lar si cal
pip install --upgrade black isort
```

### Errors de flake8

Alguns errors comuns i com solucionar-los:

```python
# E501: line too long
# Solució: deixar que black ho gestioni o partir la línia

# E203: whitespace before ':'
# Solució: ja està configurat per ignorar-se amb black

# F401: imported but unused
# Solució: eliminar l'import o marcar-lo amb # noqa: F401
```

### Errors de mypy

```python
# Type hints manuals
def my_function(param: str) -> int:
    return len(param)

# Per ignorar errors específics
variable = something()  # type: ignore

# Ignorar un fitxer sencer (afegir al principi)
# type: ignore
```

### Warnings de Bandit

```python
# Si és un fals positiu, usar # nosec
sql = "SELECT * FROM table"  # nosec B608

# O configurar skip a pyproject.toml
[tool.bandit]
skips = ["B101", "B601"]
```

## 📚 Referències

- [Black Documentation](https://black.readthedocs.io/)
- [isort Documentation](https://pycqa.github.io/isort/)
- [Flake8 Documentation](https://flake8.pycqa.org/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [Bandit Documentation](https://bandit.readthedocs.io/)
- [pre-commit Documentation](https://pre-commit.com/)

## ❓ Ajuda

Per veure totes les comandes disponibles:

```bash
make help
```

O llegir el Makefile:

```bash
cat Makefile
```
