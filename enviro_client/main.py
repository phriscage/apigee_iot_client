# pylint: disable=broad-except,invalid-name,wrong-import-position
"""
    EnviroPhat client
"""
# import os
# import sys
import argparse
import logging

from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from config import GATEWAY_HOSTNAME, OAUTH_TOKEN_URL, PROTECTED_URL
from compliance_fixes.apigee import apigee_compliance_fix

logger = logging.getLogger(__name__)


def _validate():
    """ verify the hostname is defined """
    if not GATEWAY_HOSTNAME:
        raise Exception("GATEWAY_HOSTNAME is required")


def main(**kwargs):
    """ run the main logic """
    logger.info("Starting...")
    _validate()
    client = BackendApplicationClient(
        client_id=kwargs['client_id']
    )
    session = OAuth2Session(client=client)
    session = apigee_compliance_fix(session)
    session.fetch_token(
        token_url=OAUTH_TOKEN_URL,
        client_id=kwargs['client_id'],
        client_secret=kwargs['client_secret']
    )
    session.get(PROTECTED_URL)
    logger.info("Finished.")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.DEBUG,
        format=("%(asctime)s %(levelname)s %(name)s[%(process)s] : %(funcName)s"
                " : %(message)s"),
        # filename='/var/log/cpage/%s.log' % FILE_NAME
    )
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--client_id", help="OAuth Client ID/Key",
                        type=str, dest="client_id", required=True)
    parser.add_argument("-s", "--client_secret", help="OAuth Client Secret",
                        type=str, dest="client_secret", required=True)
    parser.add_argument("-u", "--protected_url", help="Protected URL",
                        type=str, dest="protected_url", default=PROTECTED_URL)
    kwargs = parser.parse_args()
    main(**kwargs.__dict__)
