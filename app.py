from flask import Flask, json, render_template, request, redirect, url_for
import os
import json
from markupsafe import escape

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

def save_data(data):
    """Write all blog posts to the JSON storage file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def next_id(posts):
    """Generate a unique id (highest existing id + 1)."""
    return max((post.get("id", 0) for post in posts), default=0) + 1

@app.get('/')
def index():
    posts = read_data()
    return render_template('index.html', posts=posts)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        author = escape(request.form.get('author','').strip())
        title = escape(request.form.get('title', '').strip())
        content = escape(request.form.get('content', '').strip())
        ok = (author and title and content)
        if not ok:
            #todo: show error message and give posibility to fix it
            return render_template("add.html", {
                'author':author,
                'title':title,
                'content': content
            })
        data = read_data()
        #todo: sanitize data / prevent xss
        data.append({
            "id": next_id(data),
            "author": author,
            "title": title,
            "content": content,
            "likes": 0,
        })
        save_data(data)
        return redirect(url_for("index"))
    return render_template('add.html', post={})

if __name__ == '__main__':
    app.run(debug=True)


