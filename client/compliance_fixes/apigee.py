from json import loads, dumps

from oauthlib.common import to_unicode


def apigee_compliance_fix(session):

    def _wrong_token_type(r):
        token = loads(r.text)
        if token.get('token_type', None) and \
                token.get('token_type') == 'BearerToken':
            token['token_type'] = 'Bearer'
        r._content = to_unicode(dumps(token)).encode('UTF-8')
        return r

    # session._client.default_token_placement = 'query'
    session.register_compliance_hook('access_token_response',
                                     _wrong_token_type)
    return session
