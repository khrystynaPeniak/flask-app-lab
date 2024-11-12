import datetime
from . import post_bp
from flask import render_template, abort, flash, url_for, redirect, session
from .forms import PostFrom
import json

def load_posts():
    try:
        with open('app/posts.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_posts(posts):
    with open('app/posts.json', 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=4, default=str)


@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostFrom()
    if form.validate_on_submit():
        posts = load_posts()
        new_post = {
            "id": len(posts) + 1,
            "title": form.title.data,
            "content": form.content.data,
            "is_active": form.is_active.data,
            "publish_date": form.publish_date.data.strftime('%Y-%m-%d'),
            "category": form.category.data,
            "author": session.get('username'),
        }
        posts.append(new_post)
        save_posts(posts)
        
        flash(f"Post '{form.title.data}' added successfully!", "success")
        return redirect(url_for(".get_posts"))
        
    return render_template("add_post.html", form=form)
    


@post_bp.route('/') 
def get_posts():
    posts = load_posts()
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>') 
def detail_post(id):
    posts = load_posts()
    post = next((post for post in posts if post['id'] == id), None)
    if post is None:
        abort(404)
    return render_template("detail_post.html", post=post)