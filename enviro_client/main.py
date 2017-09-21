# pylint: disable=broad-except,invalid-name,wrong-import-position
"""
    EnviroPhat client
"""
# import os
# import sys
import argparse
import logging
import time
from urllib.parse import urlparse

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session
from compliance_fixes.apigee import apigee_compliance_fix

from envirophat import leds
from config import OAUTH_TOKEN_URL, PROTECTED_URL, INTERVAL, \
    CLIENT_ID, CLIENT_SECRET
from envirophat_data import EnviroPhatData

logger = logging.getLogger(__name__)


def _validate(**kwargs):
    """ verify the required variables are defined """
    print(kwargs)
    for required in ('CLIENT_ID', 'CLIENT_SECRET', 'OAUTH_TOKEN_URL',
                     'PROTECTED_URL'):
        if not kwargs.get(required.lower(), None):
            raise Exception("'%s' is None" % required)
    for url in ('OAUTH_TOKEN_URL', 'PROTECTED_URL'):
        parsed_url = urlparse(kwargs.get(url.lower()))
        if not bool(parsed_url.scheme) or not bool(parsed_url.netloc):
            raise Exception(
                "'%s' is not a valid URL: '%s'" % (url, kwargs.get(url.lower()))
            )


def main(**kwargs):
    """ run the main logic """
    logger.info("Starting...")
    _validate(**kwargs)
    client = BackendApplicationClient(
        client_id=kwargs['client_id']
    )
    session = OAuth2Session(client=client)
    session = apigee_compliance_fix(session)
    session.fetch_token(
        token_url=kwargs['oauth_token_url'],
        client_id=kwargs['client_id'],
        client_secret=kwargs['client_secret']
    )
    leds.off()
    while True:
        if kwargs['leds']:
            leds.on()
        data = EnviroPhatData.get_sample()
        if kwargs['leds']:
            leds.off()
        session.post(PROTECTED_URL, data=data)
        logger.debug("Sleeping for '%d' seconds..." % kwargs['internval'])
        time.sleep(kwargs['internval'])
    logger.info("Finished.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format=("%(asctime)s %(levelname)s %(name)s[%(process)s] : %(funcName)s"
                " : %(message)s"),
        # filename='/var/log/cpage/%s.log' % FILE_NAME
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("-c_i", "--client_id", help="OAuth Client ID/Key",
                        type=str, dest="client_id", default=CLIENT_ID)
    parser.add_argument("-c_s", "--client_secret", help="OAuth Client Secret",
                        type=str, dest="client_secret", default=CLIENT_SECRET)
    parser.add_argument("-t_u", "--oauth_token_url", help="OAuth Token URL",
                        type=str, dest="oauth_token_url",
                        default=OAUTH_TOKEN_URL)
    parser.add_argument("-p_u", "--protected_url", help="Protected URL",
                        type=str, dest="protected_url", default=PROTECTED_URL)
    parser.add_argument("-i", "--internval", help="Sample Interval (seconds)",
                        type=int, dest="internval", default=INTERVAL)
    parser.add_argument("-l", "--leds", help="Turn LEDs On/Off between samples",
                        type=bool, dest="leds", default=False)
    kwargs = parser.parse_args()
    main(**kwargs.__dict__)
