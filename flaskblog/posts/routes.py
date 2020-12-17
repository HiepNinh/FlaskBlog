# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 13:31:23 2020

@author: ADMIN
"""
from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from databases import db
from databases.models import Post
from flaskblog.posts.forms import PostForm


posts = Blueprint('posts', __name__)


@posts.route("/post/create", methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('You just have posted successfully', 'success')
        return redirect(url_for('main.home'))
    return render_template('posts/create_post.html', title='Create Post', form=form, legend='Create New Post')


@posts.route("/post/view/<int:post_id>")
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('posts/view_post.html', title=post.title, post=post)


@posts.route("/post/update/<int:post_id>", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('You just have updated post successfully', 'success')
        return redirect(url_for('posts.view_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('posts/create_post.html', title='Update Post', form=form, legend='Update Post')


@posts.route("/post/delete/<int:post_id>", methods=['GET', 'POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('You just have deleted post successfully', 'success')
    return redirect(url_for('main.home'))

