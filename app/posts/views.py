from . import post_bp
from flask import render_template, abort, flash, url_for, redirect, session, request
from .forms import PostFrom
from .utils import load_posts, save_post, get_post

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostFrom()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        publish_date = form.publish_date.data.strftime('%d.%m.%Y')
        category = form.category.data
        is_active = form.is_active.data
        author = session.get('username')
        new_post = {"id": len(load_posts()) + 1, 'title': title, 'content': content, 'publish_date': publish_date,
                    'category': category, 'author': author, 'is_active': is_active}
        save_post(new_post)
        flash(f"Post {title} added successfully!", "success")
        return redirect(url_for(".get_posts"))
    elif request.method == "POST":
        flash(f"Enter the correct data in the form!", "danger")
    return render_template("add_post.html", form=form)
    


@post_bp.route('/') 
def get_posts():
    posts = load_posts()
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>') 
def detail_post(id):
    post = get_post(id)
    if post is None:
        abort(404)
    return render_template("detail_post.html", post=post)