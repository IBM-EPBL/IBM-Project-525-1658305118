from unicodedata import name
from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)


@app.route("/")
def home_page():
    return render_template('index.html')


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/signup")
def sign_up():
    return render_template('signup.html')


@app.route("/signin")
def sign_in():
    return render_template('signin.html')


'''@app.route("/")
def hello_world():
    return "<h1>Home page</h1>"


@app.route("/hello/<name>")
def hello_name(name):
    return render_template('hello.html', myname=name)
    # return "<h1>Hello %s!</h1>" % name


@app.route("/page/<int:numbers>")
def page_number(numbers):
    # return "<h1>page no. %d</h1>" % numbers
    return render_template('page.html', pageno=numbers)


@app.route("/admin")
def admin():
    return render_template('admin.html')


@app.route('/user/<name>')
def hello_user(name):
    if name == 'admin':
        return redirect(url_for('admin'))
    else:
        return redirect(url_for('hello_name', name=name))


@app.route("/about")
def about():
    return "<h1>about page</h1>"


@app.route("/register")
def register():
    return "<h1>register page</h1>"'''


if __name__ == '__main__':
    app.run(debug=True)
