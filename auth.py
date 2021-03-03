import os
from functools import wraps
import json
from urllib.request import urlopen
from jose import jwt
from flask import request, _request_ctx_stack

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
API_AUDIENCE = os.environ['AUTH0_API_AUDIENCE']
ALGORITHMS = ['RS256']


# Error handler
class AuthError(Exception):

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    """Obtains the Access Token from the Authorization Header.
    Code derived from https://auth0.com/docs/quickstart/backend/python.
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError('authorization header is expected', 401)

    parts = auth.split()

    if parts[0].lower() != 'bearer':
        raise AuthError('authorization header must start with Bearer', 401)
    elif len(parts) == 1:
        raise AuthError('token not found', 401)
    elif len(parts) > 2:
        raise AuthError('authorization header must be Bearer token', 401)

    token = parts[1]
    return token


def verify_decode_jwt(token):
    """Verify a JWT for the Coffee Shop app. Code mostly from https://auth0.com/docs/quickstart/backend/python.

    :param token: A json web token (string)
    :returns: The decoded payload
    :raises AuthError: 401 if error decoding jwt or invalid signature
    """
    jsonurl = urlopen('https://' + AUTH0_DOMAIN + '/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    try:
        unverified_header = jwt.get_unverified_header(token)
    except Exception:
        raise AuthError('error decoding token headers', 401)
    rsa_key = {}
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            # Returns the payload if the JWT is valid.
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError('token is expired', 401)
        except jwt.JWTClaimsError:
            raise AuthError('incorrect claims, please check the audience and issuer', 401)
        except Exception:
            raise AuthError('unable to parse authentication token', 401)
    else:
        raise AuthError('unable to find appropriate key', 401)


def check_permissions(permission, payload):
    """Determines if the JWT payload includes a permission.

    :param permission: String permission (i.e. 'view:movie')
    :param payload: Decoded jwt payload
    :returns: True if not permissions required or payload has the permissions required
    :raises AuthError: 401 if permissions are not included in the payload.
        403 if the requested permission string is not in the payload permissions array.
    """
    # Return True if no permission (eg. None or empty string)
    if permission:
        if 'permissions' not in payload:
            raise AuthError('permissions not in payload', 401)
        if permission not in payload['permissions']:
            raise AuthError('permission not found', 403)
    return True


def requires_auth(permission=None):
    """Determines if the Access Token is valid.
    Code from https://auth0.com/docs/quickstart/backend/python.
    """
    def requires_auth_decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            _request_ctx_stack.top.current_user = payload
            check_permissions(permission, payload)
            return f(*args, **kwargs)
        return decorated
    return requires_auth_decorator
