# pylint: disable=broad-except,invalid-name,wrong-import-position
"""
    EnviroPhat client model
"""
import os
import sys
import logging
import time
from urllib.parse import urlparse
import simplejson as json

from oauthlib.oauth2 import BackendApplicationClient
from oauthlib.oauth2.rfc6749.errors import TokenExpiredError
from requests_oauthlib import OAuth2Session

from compliance_fixes.apigee import apigee_compliance_fix
from envirophat import leds

sys.path.insert(0, os.path.dirname(
    os.path.realpath(__file__)) + '/../../lib')

from enviro.data import EnviroPhatData # noqa

logger = logging.getLogger(__name__)


class EnviroPhatClient(object):
    """ encapsulate EnviroPhat client in a class """

    def __init__(self, **kwargs):
        """ instantiate the class """
        self.required = ('CLIENT_ID', 'CLIENT_SECRET', 'OAUTH_TOKEN_URL',
                         'PROTECTED_URL')
        self.kwargs = kwargs
        self._validate(self.kwargs)

    def _validate(self, kwargs):
        """ verify the required variables are defined """
        print(kwargs)
        for required in self.required:
            if not kwargs.get(required.lower(), None):
                raise AttributeError(
                    "'%s/%s' is None" % (required, required.lower())
                )
        for url in ('OAUTH_TOKEN_URL', 'PROTECTED_URL'):
            parsed_url = urlparse(kwargs.get(url.lower()))
            scheme = parsed_url.scheme
            netloc = parsed_url.netloc.split(':')[0]
            if not bool(scheme) or not bool(netloc) \
                    or scheme == 'None' or netloc == 'None':
                raise AttributeError(
                    "'%s/%s' is not a valid URL: '%s'" % (
                        url, url.lower(), kwargs.get(url.lower())
                        )
                )

    def run(self):
        """ run the main logic """
        logger.info("Starting...")
        client = BackendApplicationClient(
            client_id=self.kwargs['client_id']
        )
        client_creds = {
            'client_id': self.kwargs['client_id'],
            'client_secret': self.kwargs['client_secret']
        }
        session = OAuth2Session(
            client=client,
            # not enabled for client_credentials grant
            # auto_refresh_url=kwargs['oauth_token_refresh_url'],
            # auto_refresh_kwargs=client_creds
        )
        session = apigee_compliance_fix(session)
        session.fetch_token(
            token_url=self.kwargs['oauth_token_url'],
            **client_creds
        )
        leds.off()
        while True:
            if self.kwargs['leds']:
                leds.on()
            data = EnviroPhatData.get_sample()
            if self.kwargs['leds']:
                leds.off()
            try:
                # 'application/x-www-form-urlencoded'
                # session.post(self.kwargs['protected_url'], data=data)
                req = session.post(
                    self.kwargs['protected_url'], data=json.dumps(data)
                )
            except TokenExpiredError:
                logger.info("Trying to fetch OAuth token again...")
                session.fetch_token(
                    token_url=self.kwargs['oauth_token_url'],
                    **client_creds
                )
                session.post(self.kwargs['protected_url'], data=data)
            if req.status_code not in [200, 201]:
                logger.warn(req.text)
                raise RuntimeError(
                    "incorrect status code '%i'" % req.status_code
                )
            logger.debug(
                "Sleeping for '%d' seconds..." % self.kwargs['internval']
            )
            time.sleep(self.kwargs['internval'])
        logger.info("Finished.")
