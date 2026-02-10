"""Defines a NationBuilder API **Donations** interface."""

from nationbuilder_api.endpoints import Endpoint
from nationbuilder_api.endpoints.decorators import handle_pagination, handle_resp_proc
from nationbuilder_api.resp_procs import payload_filter, resp_bool


class Donations(Endpoint):
    """NationBuilder API **Donations** Interface

    Methods
    -------
    __call__(**kwargs)
        Get donations.
    search(donor_id=None, event="succeeded", since=None, **kwargs)
        Get donation by donor ID, transaction date, or creation date.
    add(donation, **kwargs)
        Add donation.
    update(id, donation, **kwargs)
        Update donation.
    remove(id, **kwargs)
        Remove donation.
    """

    resource_name = "donation"

    @handle_resp_proc(payload_filter())
    @handle_pagination
    def __call__(self, **kwargs):
        """Get donations.

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
            With the default response processor, the donation resources.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request("get", "donations", **kwargs)

    @handle_resp_proc(payload_filter())
    @handle_pagination
    def search(self, donor_id=None, event="succeeded", since=None, **kwargs):
        """Get donation by donor ID, transaction date, or creation date.

        Parameters
        ----------
        donor_id : int, optional
            The donor's ID.
        event : {"succeeded", "failed", "created"}, optional
            The donation event type.
        since : str, optional
            Datetime in ``ISO 8601`` format (``YYYY-MM-DDThh:mm:ss+/-hh:mm``).
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
            With the default response processor, the donation resources.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request(
            "get",
            f"donations/search?{'donor_id=' + donor_id if donor_id else event + '_since=' + since}",
            **kwargs,
        )

    @handle_resp_proc(resp_bool)
    def add(self, donation, **kwargs):
        """Add donation.

        Parameters
        ----------
        donation : dict
            Donation representation.
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

        payload = {"donation": donation}

        return self.session.make_request("post", "donations", payload, **kwargs)

    @handle_resp_proc(resp_bool)
    def update(self, id, donation, **kwargs):
        """Update donation.

        Parameters
        ----------
        id : int
            The donation ID.
        donation : dict
            Donation representation.
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

        payload = {"donation": donation}

        return self.session.make_request("put", f"donations/{id}", payload, **kwargs)

    @handle_resp_proc(resp_bool)
    def remove(self, id, **kwargs):
        """Remove donation.

        Parameters
        ----------
        id : int
            The donation ID.
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

        return self.session.make_request("delete", f"donations/{id}", **kwargs)
