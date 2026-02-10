"""Defines a NationBuilder API **Tags** interface."""

from nationbuilder_api.endpoints import Endpoint
from nationbuilder_api.endpoints.decorators import handle_pagination, handle_resp_proc
from nationbuilder_api.resp_procs import payload_filter


class Tags(Endpoint):
    """NationBuilder API **Tags** Interface

    Methods
    -------
    __call__(**kwargs)
        Get tags.
    people(name, **kwargs)
        Get people with a given tag.
    """

    resource_name = "tag"

    @handle_resp_proc(payload_filter())
    @handle_pagination
    def __call__(self, **kwargs):
        """Get tags.

        Parameters
        ----------
        **kwargs
            Keyword arguments passed to ``NationBuilderClient.make_request``.
            `headers` will update the session level `headers` while `timeout` overrides
            the session default (see "Other Parameters") - anything else becomes a query
            parameter.

        Other Parameters
        ----------------
        max_resps : int
            The maximum number of responses to fetch.
        resp_proc : callable
            Response processor (default extracts the resources from the response:
            `payload_filter()`).
        headers : dict
            Add to or override the session level `headers`.
        timeout : int
            Override the session level request `timeout`.

        Returns
        -------
        list of dict
            With the default response processor, the tag resources.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request("get", "tags", **kwargs)

    @handle_resp_proc(payload_filter())
    @handle_pagination
    def people(self, name, **kwargs):
        """Get people with a given tag.

        Parameters
        ----------
        name : str
            The tag name.
        **kwargs
            Keyword arguments passed to ``NationBuilderClient.make_request``.
            `headers` will update the session level `headers` while `timeout` overrides
            the session default (see "Other Parameters") - anything else becomes a query
            parameter.

        Other Parameters
        ----------------
        max_resps : int
            The maximum number of responses to fetch.
        resp_proc : callable
            Response processor (default extracts the resources from the response:
            `payload_filter()`).
        headers : dict
            Add to or override the session level `headers`.
        timeout : int
            Override the session level request `timeout`.

        Returns
        -------
        list of dict
            With the default response processor, the abbreviated person resources.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request("get", f"tags/{name}/people", **kwargs)
