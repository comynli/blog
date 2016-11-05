import jwt
import logging
from webob.exc import HTTPUnauthorized
from m.security import AuthenticationProvider
from .models import User


class JWTAuthenticationProvider(AuthenticationProvider):
    def __init__(self, ctx, request):
        super().__init__(ctx, request)
        header = ctx.config.get_string('authorization.header', 'X-Authorization-Token')
        self.key = ctx.config.get_string('authorization.key', 'secret')
        self.token = request.headers.get(header)

    @property
    def principal(self):
        if self.token is None:
            raise HTTPUnauthorized()
        try:
            decoded = jwt.decode(self.token.encode(), self.key, ['HS512'])
            user_id = decoded.get('user')
            if user_id is None:
                raise HTTPUnauthorized()
            user = User.query.filter(User.id == user_id).first()
            if user is None:
                raise HTTPUnauthorized()
            return user
        except Exception as e:
            logging.error(e)
            raise HTTPUnauthorized()
