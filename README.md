# Automat FullStack Flask/Next.js Installation

- Assuming you are in your project's root directory (PYTHONFULLSTACKFLASK/)

## Virtual Environment

- Create virtual environment (if not already created)
  - Windows PS: `python -m venv env`
- Activate the virtual environment
  - Mac Bash: `source env/bin/activate`
  - Windows PS: `.\env\Scripts\Activate.ps1`

## Dependencies

- Install dependencies
  - `pip install -r requirements.txt`
- Save installed dependencies
  - `pip freeze > requirements.txt`

## Flask

- (WIP) Create a .env file in the root directory and add the following variables:
  - `FLASK_APP=appRun.py`
  - `FLASK_ENV=development`
  - `FLASK_DEBUG=1`
- Run your Flask app
  - `flask run`

## Formatting and Linting

### These tools are a WIP, currently there are a lot of changes to be made for the linting and formatting to work properly.

- This project uses [pre-commit](https://pre-commit.com/) to manage git hooks. Here are the hooks we currently have: - prettier (formatting for js, css, html), black (formatting for python), - isort (import sorting for python), - flake8 (linting for python), - black (formatting for Python).
  To install the hooks run `pre-commit install` in the root directory. To run the hooks manually run `pre-commit run --all-files`. To run the hooks on every commit run `pre-commit install --hook-type commit-msg`. To skip the hooks on a commit run `git commit -m "your message" --no-verify`.
- To uninstall the hooks from your local git repository run `pre-commit uninstall`.

## Notes

- Do not commit _pycache_, env (or other env file names like venv), pytest_cache folders to git.
- Good to know: .env, .env.development, and .env.production files should be included in your repository as they define defaults. .env\*.local should be added to .gitignore, as those files are intended to be ignored. .env.local is where secrets can be stored.
