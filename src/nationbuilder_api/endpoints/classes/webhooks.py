"""Defines a NationBuilder API **Webhooks** interface."""

from nationbuilder_api.endpoints import Endpoint
from nationbuilder_api.endpoints.decorators import handle_pagination, handle_resp_proc
from nationbuilder_api.resp_procs import payload_filter, resp_bool


class Webhooks(Endpoint):
    """NationBuilder API **Webhooks** Interface

    Methods
    -------
    __call__(**kwargs)
        Get webhooks.
    get(id, **kwargs)
        Get webhook.
    add(webhook, **kwargs)
        Add webhook.
    remove(id, **kwargs)
        Remove webhook.
    """

    resource_name = "webhook"

    @handle_resp_proc(payload_filter())
    @handle_pagination
    def __call__(self, **kwargs):
        """Get webhooks.

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
            With the default response processor, the webhook resources.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request("get", "webhooks", **kwargs)

    @handle_resp_proc(payload_filter())
    def get(self, id, **kwargs):
        """Get webhook.

        Parameters
        ----------
        id : str
            The webhook ID.
        **kwargs
            Keyword arguments passed to ``NationBuilderClient.make_request``.
            `headers` will update the session level `headers` while `timeout` overrides
            the session default (see "Other Parameters") - anything else becomes a query
            parameter.

        Other Parameters
        ----------------
        resp_proc : callable
            Response processor (default extracts the resource from the response:
            `payload_filter()`).
        headers : dict
            Add to or override the session level `headers`.
        timeout : int
            Override the session level request `timeout`.

        Returns
        -------
        dict
            With the default response processor, the webhook resource.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request("get", f"webhooks/{id}", **kwargs)

    @handle_resp_proc(resp_bool)
    def add(self, webhook, **kwargs):
        """Add webhook.

        Parameters
        ----------
        webhook : dict
            Webhook representation.
        **kwargs
            Keyword arguments passed to ``NationBuilderClient.make_request``.
            `headers` will update the session level `headers` while `timeout` overrides
            the session default (see "Other Parameters") - anything else becomes a query
            parameter.

        Other Parameters
        ----------------
        resp_proc : callable
            Response processor (default returns ``True`` if the request was successful,
            elsethe unmodified response: `resp_bool`).
        headers : dict
            Add to or override the session level `headers`.
        timeout : int
            Override the session level request `timeout`.

        Returns
        -------
        bool
            With the default response processor, ``True`` if the request was successful.
        requests.Response
            With the default response processor, the unmodified response if the request
            was unsuccessful. Without the default response processor, the unmodified
            response.
        """

        payload = {"webhook": webhook}

        return self.session.make_request("post", "webhooks", payload, **kwargs)

    @handle_resp_proc(resp_bool)
    def remove(self, id, **kwargs):
        """Remove webhook.

        Parameters
        ----------
        id : str
            The webhook ID.
        **kwargs
            Keyword arguments passed to ``NationBuilderClient.make_request``.
            `headers` will update the session level `headers` while `timeout` overrides
            the session default (see "Other Parameters") - anything else becomes a query
            parameter.

        Other Parameters
        ----------------
        resp_proc : callable
            Response processor (default returns ``True`` if the request was successful,
            elsethe unmodified response: `resp_bool`).
        headers : dict
            Add to or override the session level `headers`.
        timeout : int
            Override the session level request `timeout`.

        Returns
        -------
        bool
            With the default response processor, ``True`` if the request was successful.
        requests.Response
            With the default response processor, the unmodified response if the request
            was unsuccessful. Without the default response processor, the unmodified
            response.
        """

        return self.session.make_request("delete", f"webhooks/{id}", **kwargs)
