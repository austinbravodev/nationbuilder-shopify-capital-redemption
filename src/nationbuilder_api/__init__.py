"""Provides an extended ``requests.Session`` client for interacting with the
`NationBuilder API <https://nationbuilder.com/api_documentation>`_.

Classes
-------
NationBuilderClient
    Extends ``requests.Session`` with a NationBuilder API interface.
"""

import logging
import os

import requests

from .endpoints import endpoints
from .helpers import has_level_handler

REQUEST_METHODS = (
    "get",
    "post",
    "put",
    "delete",
)


handler = logging.StreamHandler()


class NationBuilderClient(requests.Session):
    """NationBuilder API Client

    See `requests.Session
    <https://requests.readthedocs.io/en/master/api/#request-sessions>`_ for inherited
    attributes. Can be used as a context manager.

    Attributes
    ----------
    params : dict
        Session level query parameters. Can be extended or overridden on a per request
        basis.
    headers : dict
        Session level headers. Can be extended or overridden on a per request basis.
    timeout : int or float
        Seconds to wait for a response before raising ``requests.exceptions.Timeout``.
        Can be overridden on a per request basis.
    logger : logging.Handler
        The client's logger.
    endpoints : dict
        A mapping of endpoint names to instances. Use this for endpoints assistance.
    Oauth2 : class
        Provides assistance for Oauth2. Initialized by `authenticate` (see
        **Methods** -> `authenticate`). See its **Examples** for example usage.
    auth : Oauth2
        Instance of `Oauth2`. Assigned via the `authenticate` method.

    Methods
    -------
    make_request(
        http_meth, url_path, params=None, headers=None, payload=None, timeout=None
    )
        Makes all session requests by calling `get/post/put/delete`, which are decorated
        versions of ``requests.Session.get/post/put/delete`` that handle
        NationBuilder's `Rate Limit Policy
        <https://nationbuilder.com/rate_limit_policy>`_.
    authenticate(client_id, client_secret)
        Initializer for `Oauth2`. See `Oauth2` **Examples** for usage.

    Notes
    -----
    If not used as a context manager, end the session with
    `NationBuilderClient.close()`.
    """

    base_url = "https://{}.nationbuilder.com/api/v1/"

    def __init__(
        self,
        nation=os.getenv("NB_SLUG"),
        access_token=os.getenv("NB_API_KEY"),
        params={},
        headers={},
        timeout=10,
        logger=None,
        debug=False,
    ):
        """
        Parameters
        ----------
        nation : str
            The client nation's ``slug``.
        params: dict, optional
            Session level query parameters (default is ``None``). Can be extended or
            overridden on a per request basis. Initialized with a default pagination
            limit (`int`), which defaults to the maximum number of paginated results
            NationBuilder will return in a response (100). If an API key or access
            token has been acquired, pass it as `access_token`.
        headers : dict, optional
            Session level request headers (default is ``None``). Can be extended or
            overridden on a per request basis.
        timeout : int or float, optional
            Seconds to wait for a request's response before raising
            ``requests.exceptions.Timeout`` (default is ``10``). Can be overridden on
            a per request basis.
        logger : logging.Handler, optional
            The client's logger (default is ``logging.StreamHandler``).
        debug : bool, optional
            Sets the logger's level to ``logging.DEBUG`` if ``True``, else
            ``logging.INFO`` (default is ``False``).
        """

        super().__init__()

        if nation:
            self.base_url = self.base_url.format(nation)

        if access_token:
            self.params["access_token"] = access_token

        self.timeout = float(timeout)

        self.params.update(params)
        if "limit" not in params:
            self.params["limit"] = 100
        self.headers.update(headers)

        self.logger = logger or logging.getLogger(__name__)
        if debug and not self.logger.level:
            self.logger.setLevel(logging.DEBUG)

        if not has_level_handler(self.logger):
            self.logger.addHandler(handler)

        self.endpoints = {}
        for endpoint_name, endpoint in sorted(endpoints, key=lambda item: item[0]):
            setattr(self, endpoint_name, endpoint(self))
            self.endpoints[endpoint_name] = getattr(self, endpoint_name)

    def make_request(
        self, http_meth, url_path, payload=None, headers=None, timeout=None, **params
    ):
        """Makes an authenticated request to NationBuilder's API. Logs the response to
        ``DEBUG``.

        Handles ``requests.exceptions.HTTPError``s by logging the exception to
        ``ERROR``. Handles the NationBuilder API's rate limiting.

        Parameters
        ----------
        http_meth : {'get', 'post', 'put', 'delete'}
            Case insensitive HTTP method to use.
        url_path : str
            NationBuilder API URL path to access including any URL parameters
            (e.g. "people/42").
        params : dict, optional
            Request level query parameters - will extend and override the session level
            parameters (default is ``None``).
        headers : dict, optional
            Request level headers - will extend and override the session level headers
            (default is ``None``).
        payload : dict, optional
            Resource representation to be converted to the JSON body (default is
            ``None``).
        timeout : int or float, optional
            Request level timeout - will override the client default (``10``).

        Returns
        -------
        requests.Response
            The full response object.
        """

        url = self.base_url + url_path

        resp = getattr(self, http_meth.lower())(
            url,
            params=params,
            headers=headers,
            json=payload,
            timeout=float(timeout or self.timeout),
        )
        resp.raise_for_status()

        return resp
