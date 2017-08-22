import requests
import hmac
import hashlib

from requests.auth import AuthBase

class BittrexAuth(AuthBase):
    """Sign requests to Market and Private API."""
    def __init__(self, api_secret):
        self.api_secret = api_secret

    def __call__(self, request):
        uri = request.url
        signature = hmac.HMAC(
            key=bytes(self.api_secret, 'utf-8'),
            msg=bytes(uri, 'utf-8'),
            digestmod=hashlib.sha512
        ).hexdigest()

        request.headers['apisign'] = signature
        print(request.headers)
        return request

class Client(object):
    """Create a new session to the Bittrex exchange."""
    def __init__(self, api_key, api_secret):
        self.api_version = 'v1.1'
        self.api_base = 'https://bittrex.com/api/%s' % (self.api_version)

        self.api_key = api_key
        self.api_secret = api_secret

        # create a session object
        self.session = requests.Session()

    def _get_api_version(self):
        return self.api_version

    def _build_url(self, endpoint):
        """ Helper function to build the full URL """
        return self.api_base + endpoint

    def _call(self, url, params=None):
        return self.session.get(url, params=params, auth=BittrexAuth(self.api_secret))

    # Public API Functions
    # --------------------

    def get_markets(self):
        """ Used to get the open and available trading markets at Bittrex along with other metadata."""

        url = self._build_url('/public/getmarkets')

        return self._call(url)

    def get_currencies(self):
        """ Used to get all supported currencies at Bittrex along with other metadata."""

        url = self._build_url('/public/getcurrencies')

        return self._call(url)

    def get_ticker(self, market, *args, **kwargs):
        """ Used to get the current tick values for a market."""

        url = self._build_url('/public/getticker')

        payload = {'market': market}

        return self._call(url, params=payload)

    def get_market_summaries(self):
        """ Used to get the last 24 hour summary of all active exchanges."""

        url = self._build_url('/public/getmarketsummaries')

        return self._call(url)

    def get_market_summary(self, market, *args, **kwargs):
        """ Used to get the last 24 hour summary of all active exchanges."""

        url = self._build_url('/public/getmarketsummary')

        payload = {'market': market}

        return self._call(url, params=payload)

    def get_orderbook(self, market, type, *args, **kwargs):
        """ Used to get retrieve the orderbook for a given market."""

        url = self._build_url('/public/getorderbook')

        payload = {'market': market, 'type': type}

        return self._call(url, params=payload)

    def get_market_history(self, market, *args, **kwargs):
        """ Used to retrieve the latest trades that have occured for a specific market."""

        url = self._build_url('/public/getmarkethistory')

        payload = {'market': market}

        return self._call(url, params=payload)
