# pylint: disable=broad-except,invalid-name,wrong-import-position,E402
"""
    EnviroPhat client main
"""
import os
import sys
import logging
import argparse
from config import OAUTH_TOKEN_URL, OAUTH_TOKEN_REFRESH_URL, PROTECTED_URL, \
    CLIENT_ID, CLIENT_SECRET, INTERVAL

sys.path.insert(0, os.path.dirname(
    os.path.realpath(__file__)) + '/lib')

from enviro.client import EnviroPhatClient # noqa


def main(**kwargs):
    """ main logic """
    try:
        client = EnviroPhatClient(**kwargs)
        client.run()
    except AttributeError:
        parser.print_help()
        raise
    except Exception:
        raise


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
    parser.add_argument("-tr_u", "--oauth_token_refresh_url",
                        type=str, dest="oauth_token_refresh_url",
                        help="OAuth Token Refresh URL",
                        default=OAUTH_TOKEN_REFRESH_URL)
    parser.add_argument("-p_u", "--protected_url", help="Protected URL",
                        type=str, dest="protected_url", default=PROTECTED_URL)
    parser.add_argument("-i", "--internval", help="Sample Interval (seconds)",
                        type=float, dest="internval", default=INTERVAL)
    parser.add_argument("-l", "--leds", help="Turn LEDs On/Off between samples",
                        type=bool, dest="leds", default=False)
    kwargs = parser.parse_args()
    main(**kwargs.__dict__)
