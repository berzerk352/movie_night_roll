## Random Movie Roll Script
This project is dependent on a Google OAuth token. When you run the script, a browser window will open asking if you are OK with giving permission to the script. The script then has the ability to read any Google Docs/Sheets that your account does. 

- `random_movie.ini` specifies which tab of the spreadsheet to roll through and stores the last user whose movie was selected.
- `credentials.json` stores the OAuth secret used to authenticate. This is not checked into git and will need to be manually created 
- `token.json` temporarily stores the credential to access Google docs. If the token has expired you'll have to manually delete this file and re-run the script

This project uses `uv` for package management. Simply run `pip install uv` then `uv run random_movie.py`