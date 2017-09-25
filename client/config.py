
# pylint: disable=broad-except,invalid-name
"""
    Configuration
"""
import os

CURRENT_DIR = os.path.realpath(os.path.join(os.getcwd(),
                               os.path.dirname(__file__)))

# Client credentials
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Client options
INTERVAL = int(os.getenv('INTERVAL', 2))

# Gateway configuration:
GATEWAY_HOSTNAME = os.getenv('GATEWAY_HOSTNAME')
GATEWAY_SSL_PORT = int(os.getenv('GATEWAY_SSL_PORT', 443))
GATEWAY_HOST = '%s:%i' % (GATEWAY_HOSTNAME, GATEWAY_SSL_PORT)
OAUTH_TOKEN_URL = os.getenv(
    'OAUTH_TOKEN_URL', 'https://%s/oauth/v2/token' % GATEWAY_HOST
)
OAUTH_TOKEN_REFRESH_URL = os.getenv(
    'OAUTH_TOKEN_REFRESH_URL', OAUTH_TOKEN_URL + '/refresh'
)
PROTECTED_URL = os.getenv(
    'PROTECTED_URL', 'https://%s/envirophat' % GATEWAY_HOST
)
