from flask import Flask, request, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return 'This is the homepage'


@app.route('/arbisoft')
def arbisoft():
    return '<h2>Summer internship at Arbisoft %s</h2>' % request.method


@app.route('/profile/<name>')
def profile(name):
    return render_template("profile.html", name=name)


@app.route('/post/<int:post_id>')
def post(post_id):
    return "<h2>The post ID is %s</h2>" % post_id


@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        return "<h2>You are using POST method</h2>"
    else:
        return "<h2>You are probably using GET</h2>"


if __name__ == "__main__":
    app.run(debug=True)
