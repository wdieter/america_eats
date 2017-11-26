from flask import Flask, render_template
import sqlite3

conn = sqlite3.connect('am_v1.sqlite')
c = conn.cursor()
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, Stef!'

@app.route('/how_much_i_love_you')
def how_much():
    return 'To the moon and back!'

@app.route('/<string:page_name>/')
def render_static(page_name):
    response = c.execute(f"select name, h1, description, yield from Recipes where name = '{page_name}'")
    name, h1, description, _yield = response.fetchall()[0]
    image = h1+'.jpg'
    print(image)
    return render_template('LP3.html', h1=h1, description=description, img=image)

if __name__ == '__main__':
    app.run(host='0.0.0.0')