# Automat FullStack Flask/Next.js
## Installation
### Assuming you are in your project's root directory (PYTHONFULLSTACKFLASK/)
1. Create virtual environment (if not already created)
    - Windows PS: `python -m venv env`    
2. Activate the virtual environment 
    - Mac Bash: `source env/bin/activate`
    - Windows PS: `.\env\Scripts\Activate.ps1`  
3. Install dependencies 
    - `pip install -r requirements.txt`
4. Create a .env file in the root directory and add the following variables
    - `FLASK_APP=appRun.py`
    - `FLASK_ENV=development`
    - `FLASK_DEBUG=1`
4. Run your Flask app
    - `flask run`   

## Development
- After installing a new pip library run `pip freeze > requirements.txt`                  

### Notes
- Do not commit _pycache_, env (or other env file names like venv), pytest_cache folders to git.
