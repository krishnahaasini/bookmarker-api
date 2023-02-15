from flask import Blueprint,request,jsonify
import validators
from src.constants import http_status_codes
from src.database import Bookmark,db, User
from flask_jwt_extended import get_jwt_identity,jwt_required



bookmarks=Blueprint('bookmarks',__name__,url_prefix='/api/v1/bookmarks')


@bookmarks.route('/',methods=['POST','GET'])
@jwt_required()
def handle_bookmarks():

    current_user=get_jwt_identity()
    if request.method == 'POST':
        body=request.get_json().get('body', '')
        url=request.get_json().get('url', '')

        if not validators.url(url):
            return jsonify({
                'error':'Enter a valid url'
            }),http_status_codes.HTTP_400_BAD_REQUEST

        if Bookmark.query.filter_by(url=url).first():
            return jsonify({
                'error':'URL already exists'
            }),http_status_codes.HTTP_409_CONFLICT

        bookmark_obj=Bookmark(url=url,body=body,user_id=current_user)

        db.session.add(bookmark_obj)
        db.session.commit()
        return jsonify({
            'message': 'Bookmark added'
        }),http_status_codes.HTTP_200_OK
    

    if request.method == 'GET':
        result = []
        user=User.query.filter_by(id=current_user).first()
        if user:
            for i in user.bookmarks:

                result.append({
                    i.id : {
                        'body':i.body,
                        'url':i.url
                        }
                    })
            return jsonify(result)
        return jsonify({
            'error':'User do not exist'
        })





