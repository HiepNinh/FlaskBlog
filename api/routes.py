from api.users.users_api import UsersApi, LoginApi, UserApi
from api.posts.posts_api import PostsApi, PostApi



def initialize_routes(api):
    api.add_resource(LoginApi, '/api/v1/login')
    api.add_resource(UsersApi, '/api/v1/users')
    api.add_resource(UserApi, '/api/v1/me')
    
    api.add_resource(PostsApi, '/api/v1/posts')
    api.add_resource(PostApi, '/api/v1/post/<id>')