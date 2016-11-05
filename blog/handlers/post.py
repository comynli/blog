import re
import datetime
import logging
from m import Router
from m.security import Require
from m.utils import jsonify
from webob import exc
from ..models import db, Post, PostContent, Catalog, Like, Favorite


router = Router('/api/post')

img_re = re.compile(r'''!\[(.*)\]\((.*)\)''')


def update_post(request, status=0):
    try:
        payload = request.json()
        post_id = payload['post']
        content = payload.get('content')
        title = payload.get('title')
        catalog_id = payload.get('catalog')
    except Exception as e:
        raise exc.HTTPBadRequest(e)
    post = Post.query.filter(Post.id == post_id).first_or_404()
    if post.author_id != request.principal.id:
        raise exc.HTTPForbidden('it is not your post')
    if post.status != 0:
        raise exc.HTTPBadRequest('post is published or deleted')
    if title is not None:
        post.title = title
    if catalog_id is not None:
        catalog = Catalog.query.filter(Catalog.id == catalog_id).first()
        if catalog is not None:
            post.catalog = catalog
    if content is not None:
        for line in content.splitlines():
            m = img_re.search(line)
            if m:
                first_image = m.group(2)
                post.image = first_image
                break
        post_content = PostContent.query.filter(PostContent.id == post.id).first()
        if post_content is None:
            post_content = PostContent(content=content)
        post_content.content = content
        post.content = post_content
    post.timestamp = datetime.datetime.now()
    post.status = status
    db.session.add(post)
    try:
        db.session.commit()
    except Exception as e:
        raise exc.HTTPInternalServerError(e)
    return jsonify(code=200, post=post.dictify(exclude={'author.password', 'author.catalogs'}))


@router.put('')
@Require()
def create(ctx, request):
    user = request.security.principal
    catalog_id = int(request.params.get('catalog'))
    catalog = Catalog.query.filter(Catalog.id == catalog_id).first_or_404('catalog not found')
    post = Post(author=user, catalog=catalog, timestamp=datetime.datetime.now())
    db.session.add(post)
    try:
        db.session.commit()
        return jsonify(code=200, post=post.dictify(relationships=False))
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        raise exc.HTTPInternalServerError(e)


@router.put('/draft')
@Require()
def draft(ctx, request):
    return update_post(request)


@router.put('/publish')
@Require()
def publish(ctx, request):
    return update_post(request, 1)


@router.put('/edit/{id:int}')
@Require()
def edit(ctx, request):
    post = Post.query.filter(Post.id == request.args['id']).first_or_404()
    if post.author_id != request.principal.id:
        raise exc.HTTPForbidden('it is not your post')
    post.status = 0
    db.session.add(post)
    try:
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        raise exc.HTTPInternalServerError(e)
    return jsonify(code=200, post=post.dictify(exclude={'author.password', 'author.catalogs'}))


@router.get('/{id:int}')
def get(ctx, request):
    post = Post.query.filter(Post.id == request.args['id']).first_or_404()
    if post.status != 1:
        if request.principal is None or request.principal.id != post.author.id:
            raise exc.HTTPNotFound('post not exist or deleted')
    return jsonify(code=200, post=post.dictify(exclude={'author.password', 'author.catalogs'}))


@router.get('')
def get_all(ctx, request):
    page = request.params.get('page', 1)
    size = request.params.get('size', 50)
    posts = Post.query.filter(Post.status == 1).paginate(page, size)
    return jsonify(code=200, posts=posts.dictify(exclude={'author.password', 'author.catalogs'}))


@router.get('/user/{id:int}')
def get_by_user(ctx, request):
    page = request.params.get('page', 1)
    size = request.params.get('size', 50)
    posts = Post.query.filter(Post.status == 1).filter(Post.author_id == request.args['id']).paginate(page, size)
    return jsonify(code=200, posts=posts.dictify(exclude={'author.password', 'author.catalogs'}))


@router.get('/catalog/{id:int}')
def get_by_catalog(ctx, request):
    page = request.params.get('page', 1)
    size = request.params.get('size', 50)
    posts = Post.query.filter(Post.status == 1).filter(Post.catalog_id == request.args['id']).paginate(page, size)
    return jsonify(code=200, posts=posts.dictify(exclude={'author.password', 'author.catalogs'}))


@router.delete('/{id:int}')
@Require()
def delete(ctx, request):
    post = Post.query.filter(Post.id == request.args['id']).first_or_404()
    if post.author_id != request.principal.id:
        raise exc.HTTPForbidden('it is not your post')
    post.status = 2
    db.session.add(post)
    try:
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        raise exc.HTTPInternalServerError(e)
    return jsonify(code=200, post=post.dictify(exclude={'author.password', 'author.catalogs'}))


@router.put('/{id:int}')
@Require()
def like(ctx, request):
    post = Post.query.filter(Post.id == request.args['id']).first_or_404()
    user = request.principal
    _like = Like.query.filter(Like.post_id == post.id).filter(Like.user_id == user.id).first()
    if _like is None:
        _like = Like(post_id=post, user_id=user)
    db.session.add(_like)
    try:
        db.session.commit()
    except Exception as e:
        logging.error(e)
        db.session.rollback()
        raise exc.HTTPInternalServerError(e)
    return jsonify(code=200)