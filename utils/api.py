import aiohttp
import base64
from urllib.parse import urlencode

from utils.log import Logger


class SonarrAPI:
    def __init__(
            self,
            hostname: str,
            api_key: str,
            port: int = 8989,
            url_base: str = '',
            ssl: bool = False,
    ):
        logger = Logger.get_logger()
        logger.info("Initializing SonarrAPI")

        if not hostname:
            logger.error("Hostname is missing")
            raise ValueError('Hostname is required')

        if not api_key.isalnum() or len(api_key) != 32:
            logger.error("Invalid API key format")
            raise ValueError('Invalid API Key')

        self.hostname = hostname.replace('http://', '').replace('https://', '')
        self.api_key = api_key
        self.port = port
        self.url_base = url_base if url_base.startswith('/') else '/' + url_base
        self.ssl = ssl

        self.server_url = f"http{'s' if ssl else ''}://{self.hostname}:{self.port}{self.url_base}"
        self.server_api = f"{self.server_url}api/"
        logger.info(f"SonarrAPI initialized with server URL: {self.server_url}")

    async def _request(self, actions):
        logger = Logger.get_logger()

        api_url = self.server_api + actions['relativeUrl']
        if actions.get('parameters') and actions['method'] != 'POST':
            api_url += '?' + urlencode(actions['parameters'])

        headers = {
            'X-API-KEY': self.api_key
        }

        if actions['method'] == 'GET':
            headers['Accept'] = 'application/json'
        else:
            headers['Content-Type'] = 'application/json'

        logger.debug(f"Making {actions['method']} request to: {api_url}")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(actions['method'], api_url, headers=headers, json=actions.get('parameters'), ssl=self.ssl) as response:
                    if response.status == 401:
                        logger.error(f"Unauthorized: Invalid API Key for URL: {api_url}")
                        raise ValueError('Unauthorized: Invalid API Key')

                    if response.status == 200 and 'application/json' not in response.headers.get('Content-Type', ''):
                        logger.debug("Request successful (non-JSON response)")
                        return "success"

                    if response.status == 200:
                        logger.debug("Request successful with JSON response")
                        return await response.json()

                    error_text = await response.text()
                    logger.error(f"Request failed with status {response.status}: {error_text}")
                    raise ValueError(f'Error: Status {response.status}')
        except aiohttp.ClientError as e:
            logger.error(f"Network error during request: {str(e)}")
            raise

    async def get(self, relative_url, parameters=None):
        logger = Logger.get_logger()
        logger.debug(f"Preparing GET request to {relative_url}")

        if relative_url is None:
            logger.error("Relative URL is not set")
            raise TypeError('Relative URL is not set')

        if parameters is not None and not isinstance(parameters, dict):
            logger.error("Invalid parameters type")
            raise TypeError('Parameters must be type object')

        actions = {
            'relativeUrl': relative_url,
            'method': 'GET',
            'parameters': parameters
        }

        return await self._request(actions)

    async def post(self, relative_url, parameters=None):
        logger = Logger.get_logger()
        logger.debug(f"Preparing POST request to {relative_url}")

        if relative_url is None:
            logger.error("Relative URL is not set")
            raise TypeError('Relative URL is not set')

        if parameters is not None and not isinstance(parameters, dict):
            logger.error("Invalid parameters type")
            raise TypeError('Parameters must be type object')

        actions = {
            'relativeUrl': relative_url,
            'method': 'POST',
            'parameters': parameters
        }

        return await self._request(actions)

    async def put(self, relative_url, parameters=None):
        logger = Logger.get_logger()
        logger.debug(f"Preparing PUT request to {relative_url}")

        if relative_url is None:
            logger.error("Relative URL is not set")
            raise TypeError('Relative URL is not set')

        if parameters is not None and not isinstance(parameters, dict):
            logger.error("Invalid parameters type")
            raise TypeError('Parameters must be type object')

        actions = {
            'relativeUrl': relative_url,
            'method': 'PUT',
            'parameters': parameters
        }

        return await self._request(actions)

    async def delete(self, relative_url, parameters=None):
        logger = Logger.get_logger()
        logger.debug(f"Preparing DELETE request to {relative_url}")

        if relative_url is None:
            logger.error("Relative URL is not set")
            raise TypeError('Relative URL is not set')

        if parameters is not None and not isinstance(parameters, dict):
            logger.error("Invalid parameters type")
            raise TypeError('Parameters must be type object')

        actions = {
            'relativeUrl': relative_url,
            'method': 'DELETE',
            'parameters': parameters
        }

        return await self._request(actions)