# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 13:32:50 2020

@author: ADMIN
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    picture = FileField('Upload Post Picture', 
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Post')