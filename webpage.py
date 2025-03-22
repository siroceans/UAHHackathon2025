from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    return "Hello World"

if __name__ == '__main__':
    app.run()