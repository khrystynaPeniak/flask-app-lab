from . import post_bp
from flask import render_template, abort, flash, url_for, redirect, session, request
from .forms import PostForm
from .models import Post, Tag
from app import db
from ..users.models import User

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    
    authors = User.query.all()
    form.author.choices = [(author.id, author.username) for author in authors]
    
    tags = Tag.query.all()
    form.tags.choices = [(tag.id, tag.name) for tag in tags]
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        date_posted = form.publish_date.data
        category = form.category.data
        is_active = form.is_active.data
        
        author_id = form.author.data
        author = User.query.get(author_id)
        tags = form.tags.data
        new_post = Post(title=title, content=content, date_posted=date_posted, category=category, is_active=is_active, author=author)
        
        for tag_to_append in tags:
            tag = Tag.query.get(tag_to_append)
            new_post.tags.append(tag)
        
        db.session.add(new_post)
        db.session.commit()
        
        flash(f"Post {title} added successfully!", "success")
        return redirect(url_for(".get_posts"))
    elif request.method == "POST":
        flash(f"Enter the correct data in the form!", "danger")
    return render_template("add_post.html", form=form)
    

@post_bp.route('/') 
def get_posts():
    stmt = db.select(Post).order_by(Post.date_posted.desc())
    posts = db.session.scalars(stmt).all()
    return render_template("posts.html", posts=posts)

@post_bp.route('/<int:id>') 
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template("detail_post.html", post=post)

@post_bp.route('/delete/<int:id>', methods=["POST"])
def delete_post(id):
    post = db.get_or_404(Post, id)
    
    db.session.delete(post)
    db.session.commit()
    
    flash(f"Post '{post.title}' was successfully deleted!", "success")
    return redirect(url_for('.get_posts'))

@post_bp.route('/edit/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    post = db.get_or_404(Post, post_id)
    form = PostForm(obj=post)
    form.publish_date.data = post.date_posted
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.category = form.category.data
        
        db.session.commit()
        
        flash('Post updated successfully!', 'success')
        return redirect(url_for('.get_posts'))
    return render_template('add_post.html', form=form)