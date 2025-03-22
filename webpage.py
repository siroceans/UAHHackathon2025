import mimetypes
mimetypes.add_type('application/javascript', '.js')
mimetypes.add_type('text/css', 'css')

from flask import Flask, render_template, redirect, request

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def home():
    name = request.form.get("name")
    print("Name entered:", name)
    return render_template("homepage.html")

if __name__ == '__main__':
    app.run()