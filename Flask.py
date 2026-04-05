# ...existing code...
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello world welcome to the AI world"

if __name__ == '__main__':
    app.run(debug=True)
# ...existing code...