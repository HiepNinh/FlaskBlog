from flask import request
from flask_restful import Resource
from databases import db
from databases.models import Post
from flask_jwt_extended import jwt_required, get_jwt_identity



class PostsApi(Resource):
    def get(self):
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 5, type=int)
        posts = [result.serialized for result in Post.query.paginate(page=page, per_page=page_size).items]
        return posts, 200
    
    @jwt_required
    def post(self):
        user_id = get_jwt_identity()
        body = request.get_json()
        post = Post(title=body.get('title'), content=body.get('content'), user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return {'id': str(post.id)}, 200


class PostApi(Resource):
    def get(self, id):
        post = Post.query.get_or_404(id)
        return post.serialized, 200
    
    @jwt_required
    def put(self, id):
        post = Post.query.get_or_404(id)
        user_id = get_jwt_identity()
        if int(post.user_id) != int(user_id):
            return {'error': "You don't have permission"}, 403
        body = request.get_json()
        post.title = body.get('title')
        post.content = body.get('content')
        db.session.commit()
        return '', 200
    
    @jwt_required
    def delete(self, id):
        post = Post.query.get_or_404(id)
        user_id = get_jwt_identity()
        if int(post.user_id) != int(user_id):
            return {'error': "You don't have permission"}, 403
        db.session.delete(post)
        db.session.commit()
        return '', 200


