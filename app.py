from flask import Flask, json, render_template, request, redirect, url_for, jsonify
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
    with open('data.json', 'r') as f:
        return json.load(f)

def save_data(data):
    """Write all blog posts to the JSON storage file."""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)
    return True

def next_id(data):
    """Generate a unique id (highest existing id + 1)."""
    return max((post.get("id", 0) for post in data), default=0) + 1

#index allowes us data.pop(index) with no iteration O(1)
def index_of_item_with(key, val, data):
    """Return first data item that has passed key with value"""
    index = 0
    for item in data:
        if item.get(key) == val:
            print(f'index_of_item_with: found {key}=={val} at index: {index}')
            return index
        index += 1
    return -1

def fetch_post_by_id(id, data=None):
    if not data:
        data = read_data()
    index = index_of_item_with('id', id, data)
    if index >= 0:
        return data[index]
    return None

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

@app.route('/update/<int:post_id>', methods=["GET", "POST"])
def update(post_id):
    data = read_data()
    item = fetch_post_by_id(post_id, data)
    """
    index = index_of_item_with('id', post_id, data)
    if not index >=0:
        return "Not found", 404
    item = data[index]
    """
    if request.method == "POST":
        #update item and save save data
        author = escape(request.form.get("author", "").strip())
        title = escape(request.form.get("title", "").strip())
        content = escape(request.form.get("content", "").strip())
        if not (author and title and content):
            edited = dict(item, author=author, title=title, content=content)
            return render_template("update.html", post=edited, error="Please fill in all fields.")
        item["author"] = author
        item["title"] = title
        item["content"] = content
        save_data(data)
        #redirect to listing/index
        return redirect(url_for("index"))
    #display update page with current item data
    return render_template("update.html", post=item)

@app.route('/delete/<int:post_id>', methods=["GET", "POST"])
def delete(post_id):
    data = read_data()
    index = index_of_item_with('id', post_id, data)
    if index >= 0:
        data.pop(index)
        save_data(data)
        print(f'Item at {index} deleted successfully.')
    else:
        print(f'No item found with id {post_id}.')
    return  redirect(url_for("index"))

@app.route("/like/<int:post_id>", methods=["GET", "POST"])
def like(post_id):
    print(f'id: {post_id}')
    data = read_data()
    item = fetch_post_by_id(post_id, data)
    print('item ---- '+str(item.get('id')))
    print(jsonify(item))
    if item is None:
        return "Post not found", 404
    item["likes"] = item.get("likes", 0) + 1
    save_data(data)
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run(debug=True)


