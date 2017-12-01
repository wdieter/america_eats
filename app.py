from flask import Flask, render_template, g
import sqlite3

db_path = 'am_v1.sqlite'
app = Flask(__name__)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(db_path)
        db.row_factory = make_dicts
    return db


def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.route('/')
def hello_world():
    return render_template('LP.html')

@app.route('/how_much_i_love_you')
def how_much():
    return 'To the moon and back!'


@app.route('/<string:page_name>/')
def render_recipe(page_name):
    c = get_db().cursor()
    c.execute(f"select name, h1, description, yield from Recipes where name = '{page_name}'")
    response_dict = c.fetchall()[0]
    image = response_dict['h1'] + '.jpg'
    return render_template('LP3.html',
                           h1=response_dict['h1'],
                           description=response_dict['description'],
                           image=image)


if __name__ == '__main__':
    app.run(host='0.0.0.0')