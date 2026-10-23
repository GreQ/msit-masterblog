from flask import Flask, json, render_template
import os
import json

app = Flask(__name__)

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data.json")

def read_data():
    """Reads the blog posts data from the JSON file."""
    # Check if the data file exists
    if not os.path.exists(DATA_FILE):
        raise ValueError(f'Data file {DATA_FILE} could not be found.')
        # If the file doesn't exist, return an empty list
        return []
    with open('data.json', 'r') as f:
        return json.load(f)

@app.get('/')
def index():
    posts = read_data()
    print(len(posts))
    return render_template('index.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)


