from flask import Flask, render_template, g, request
import sqlite3

db_path = 'am_v1.sqlite'
app = Flask(__name__)

def get_db():
    """ Establishes connection to the db and stores attribute on the g object
    g is the Flask general purpose variable associated with the current application process,
    as opposed to the request object.
    Get db returns the db connection."""
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_path)
        db.row_factory = make_dicts
    return db


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


def unpack(recipe, cols: list) -> dict:
    """some data for a recipe (like instructions or ingredients) are stored as strings of python iterables
    to use them as iterables they must be evaluated as code in the app - can't use eval() in jinja"""
    for col in cols:
        if recipe[col] is not None:
            recipe[col] = eval(recipe[col])
    return recipe


def make_query(s):
    query = "Select * from recipes where "
    for string in s:
        query += f"(h1 like '%{string}%' or desc_tags like '%{string}%') and "
    query = query[:-4]  # remove last 'and'
    return query


@app.teardown_appcontext
def close_connection(exception):
    """ closes the db connection when the application context is torn down (when the request finishes) """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
@app.route('/home')
def hello_world():
    """landing page template"""
    c = get_db().cursor()
    c.execute("SELECT * FROM Recipes ORDER BY RANDOM() LIMIT 10")
    recipes = c.fetchall()
    recipes = [unpack(recipe, cols=['desc_tags']) for recipe in recipes]
    return render_template('landing.html', recipes=recipes)

@app.route('/search', methods=['GET'])
def search_recipes():
    query = request.args['query'].split()
    print(query)
    c = get_db().cursor()
    c.execute(make_query(query))
    recipes = c.fetchall()
    recipes = [unpack(recipe, cols=['desc_tags']) for recipe in recipes]
    return render_template('landing.html', recipes=recipes)

@app.route('/<string:page_name>/')
def render_recipe(page_name):
    c = get_db().cursor()
    c.execute(f"select * from Recipes where name = '{page_name}'")
    recipe = unpack(c.fetchone(), cols=['ingredients', 'instructions', 'desc_tags'])

    # render template accepts only one positional arg, keyword args must be given for rest
    return render_template('LP3.html', recipe=recipe)


if __name__ == '__main__':
    app.run(host='0.0.0.0')