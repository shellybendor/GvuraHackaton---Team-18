# brave-together-reborn

### Getting started with development

1. Install Python 3.9
2. Create a Virtual Environment using `python3 -m venv venv`
3. Source the Virtual Env by running
    - `venv\Scripts\activate.bat` on Windows (Single backslash, I had formatting issues)
    - `source venv/Scripts/activate` on Linux
4. Install the prerequisites: `pip install -r requirements.txt`
5. Set your environment variables
    - `FLASK_APP` the location of the flask object. Usually `brave_together.py:app`
    - `FLASK_DEBUG` 1 or 0. Decides whether to run the app on debug mode or not. OFF BY DEFAULT.
    - `DATABASE_URI` a connection string to the desired database. Creates a local SQLite db by default named `app.db`.
    - `SECRET_KEY` a random key used for encrypting session tokens. MAKE SURE TO GENERATE A RANDOM ONE when you run the
      server in production.
6. If you want to use the local db, you need to create it.
    - Open a flask shell using `flask shell`
    - Run `db.create_all()` which creates the local SQLite DB.
    - If you want to delete all of its contents, run `db.drop_all()`
    - Note: sometimes if you change the DB schema it's best to just delete `app.db` and run `db.create_all()` again.
7. Run the app in your local environment with `flask run`. You're all set :)

### Development practices

1. **ALWAYS** work from the Virtual Environment.
2. When you install new `pip` packages, make sure to run `pip freeze > requirements.txt` so that you keep it's specific
   version in the requirements.