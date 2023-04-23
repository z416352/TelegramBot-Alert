from flask import Flask


app = Flask(__name__)
@app.route("/")
@app.route("/hello")
def hello():
    return "Hello, World! \n"

@app.route("/callback")
def test():
    return "callback \n"

if __name__ == "__main__":
    app.run(debug=True)