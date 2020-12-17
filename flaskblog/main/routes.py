# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 13:30:53 2020

@author: ADMIN
"""
from flask import render_template, request, Blueprint
from databases.models import Post


main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=5, page=page)
    return render_template('main/home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('main/about.html', title='About')
