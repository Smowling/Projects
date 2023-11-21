import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    shares = db.execute("SELECT symbol, name, shares_count, ' ' as price, ' ' as value from shares WHERE user_id = ? AND shares_count > 0", session["user_id"])
    cash = db.execute("SELECT cash from users where id = ?", session["user_id"])
    cash = cash[0]["cash"]
    total = 0
    for share in shares:
        symbol = lookup(share["symbol"])
        share["price"] = symbol["price"]
        share["value"] = symbol["price"] * share["shares_count"]
        total += share["value"]
    total += cash
    return render_template("index.html", shares=shares, cash=cash, total=total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Missing symbol", 400)
        try:
            shares = int(request.form.get("shares"))
        except ValueError:
            return apology("not int", 400)
        if not shares:
            return apology("Missing shares", 400)
        elif shares < 1:
            return apology("Negative shares", 400)
        elif not isinstance(shares, int):
            return apology("not whole number", 400)

        quote = lookup(symbol)
        if not quote:
            return apology("Symbol not found", 400)

        price = float(quote["price"]) * int(shares)
        cash = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash = cash[0]["cash"]
        if cash < price:
            return apology("Buy some money", 400)
        else:
            # all went good, we finalize transaction
            cash = float(cash-price)
            payed = db.execute("UPDATE users SET cash = ? WHERE id = ?", cash, session["user_id"])
            if payed:
                indb = db.execute("SELECT id, shares_count FROM shares WHERE user_id = ? AND symbol = ?", session["user_id"], quote["symbol"])
                if indb:
                    insert = db.execute("UPDATE shares SET shares_count = ? WHERE id = ?", int(indb[0]["shares_count"]) + int(shares), indb[0]["id"])
                    db.execute("INSERT INTO history (user_id, symbol, name, shares_count, price, type) VALUES (?, ?, ?, ?, ?, ?)",
                                session["user_id"], quote["symbol"], quote["name"], shares, quote["price"], 1)
                else:
                    insert = db.execute("INSERT INTO shares (user_id, symbol, name, shares_count) VALUES (?, ?, ?, ?)",
                            session["user_id"], quote["symbol"], quote["name"], shares )
                    db.execute("INSERT INTO history (user_id, symbol, name, shares_count, price, type) VALUES (?, ?, ?, ?, ?, ?)",
                                session["user_id"], quote["symbol"], quote["name"], shares, quote["price"], 1)
                if insert:
                    return redirect("/")
                    #return render_template("buy.html", shares=shares, name=quote["name"], price=price)
                else:
                    return apology("Error while procesing shares", 400)
            else:
                return apology("There was an error with payment", 400)
    else:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history = db.execute("SELECT symbol, name, shares_count * type as shares, shares_count * price as total, price, created_at FROM history WHERE user_id = ?", session["user_id"])
    return render_template("history.html", history=history)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))
        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 400)
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Redirect user to home page
        return redirect("/")
    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()
    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    if request.method == "POST":
        symbol = request.form.get("symbol")
        quote = lookup(symbol)
        if not quote:
            return apology("Missing symbol", 400)
        else:
            return render_template("quote.html", name=quote["name"], price=quote["price"], symbol=quote["symbol"])
    else:
        return render_template("quote.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        username = request.form.get("username")
        usernames = db.execute("SELECT username FROM users")
        usernames = [ username["username"] for username in usernames ]
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        # Ensure username was submitted and its not in db
        if not username:
            return apology("must provide username", 400)
        elif username in usernames:
            return apology("we have this username already", 400)
        # Ensure password was submitted and pws=pws2
        elif not password:
            return apology("must provide password", 400)
        elif not confirmation:
            return apology("must repeat password", 400)
        elif not password == confirmation:
            return apology("passwords doesnt match", 400)
        # all submited data is correct
        else:
            hash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            return render_template("login.html", accountCreated="Your account was created.")

    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        try:
            shares_id = int(request.form.get("symbol"))
        except:
            return apology("Pick shares to sell", 400)
        try:
            shares_amount = int(request.form.get("shares"))
        except:
            return apology("You missed amount to sell", 400)

        symbol = db.execute("SELECT symbol, shares_count FROM shares where id = ?", shares_id)
        if int(symbol[0]["shares_count"]) < shares_amount:
            return apology("Not enough stocks", 400)
        # get symbols value and calculate cash
        symbol_current_value = lookup(symbol[0]["symbol"])
        cash = db.execute("SELECT cash FROM users where id = ?", session["user_id"])
        cash[0]["cash"] += float(shares_amount * symbol_current_value["price"])
        # update users cash
        try:
            db_result = db.execute("UPDATE users SET cash = ? WHERE id = ?", cash[0]["cash"], session["user_id"])
        except:
            return apology("Error procesing cash flow", 400)
        try:
            db_result = db.execute("INSERT INTO history (user_id, symbol, name, shares_count, price, type) VALUES (?, ?, ?, ?, ?, ?)", session["user_id"], symbol_current_value["symbol"], symbol_current_value["name"], shares_amount, symbol_current_value["price"], -1)
        except:
            return apology("Error with processing history", 400)
        try:
            db_result = db.execute("UPDATE shares SET shares_count = ? WHERE id = ?", symbol[0]["shares_count"] - shares_amount, shares_id)
        except:
            return apology("Error updating shares", 400)
        symbols = db.execute("SELECT id, symbol, shares_count FROM shares WHERE user_id = ? AND shares_count > 0", session["user_id"])
        return redirect("/")

    else:
        symbols = db.execute("SELECT id, symbol, shares_count FROM shares WHERE user_id = ? AND shares_count > 0", session["user_id"])
        return render_template("sell.html", symbols=symbols)
