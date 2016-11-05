import datetime
import logging
from m import Router
from m.utils import jsonify
from m.security import Require
from webob import exc
from ..models import db, Comment, Post


router = Router('/api/comment')


@router.post('')
@Require()
def add_comment(ctx, request):
    try:
        payload = request.json()
        post_id = payload['post']
        ref_id = payload.get('ref')
        content = payload['content']
    except Exception as e:
        raise exc.HTTPBadRequest(e)
    post = Post.query.filter(Post.id == post_id).first_or_404('post {} not found'.format(post_id))
    ref = None
    if ref_id is not None:
        ref = Comment.query.filter(Comment.id == ref_id).first()
    comment = Comment(content=content, user=request.principal, ref=ref, post_id=post.id, timestamp=datetime.datetime.now())
    db.session.add(comment)
    try:
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        raise exc.HTTPInternalServerError(e)
    return jsonify(code=200, comment=comment.dictify(exclude={'user.password', 'user.catalogs'}))


@router.get('/post/{id:int}')
def get_all(ctx, request):
    page = request.params.get('page', 1)
    size = request.params.get('size', 50)
    comments = Comment.query.filter(Comment.post_id == request.args['id']).paginate(page, size)
    return jsonify(code=200, comments=comments.dictify(exclude={'user.password', 'user.catalogs'}))
