import os
import urllib.parse
import requests
import sys

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def lookup():
    TRIVIA_URL = 'https://api.api-ninjas.com/v1/cars?make=ford'
    # Make API Call - make sure to use a valid API key.
    API_KEY = os.environ.get("API_KEY")
    resp = requests.get(TRIVIA_URL, headers={'X-Api-Key': API_KEY}).json()
    # Get first trivia result since the API returns a list of results.
    trivia = resp
    
    return trivia
