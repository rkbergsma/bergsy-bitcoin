from flask import Flask, render_template

app = Flask(__name__)

if __name__ == "__main__":
    app.run()

@app.route('/', methods=(['GET']))
def index():
    return render_template('index.html')
