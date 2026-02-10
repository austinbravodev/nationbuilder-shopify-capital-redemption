"""Defines a NationBuilder API **Lists** interface."""

from nationbuilder_api.endpoints import Endpoint
from nationbuilder_api.endpoints.decorators import handle_pagination, handle_resp_proc
from nationbuilder_api.resp_procs import payload_filter, resp_bool


class Lists(Endpoint):
    """NationBuilder API **Lists** Interface

    Methods
    -------
    __call__(**kwargs)
        Get lists.
    people(id, **kwargs)
        Get people in a list.
    add(list, **kwargs)
        Add list.
    add_people(id, people_ids, **kwargs)
        Add people to a list.
    tag(id, tag, **kwargs)
        Add a tag to all people in a list.
    export(id, context="people", **kwargs)
        Export list.
    update(id, list, **kwargs)
        Update list.
    remove(id, **kwargs)
        Remove list.
    remove_people(id, people_ids, **kwargs)
        Remove people from a list.
    remove_tag(id, tag, **kwargs)
        Remove a tag from all people in a list.
    """

    resource_name = "list"

    @handle_resp_proc(payload_filter())
    @handle_pagination
    def __call__(self, **kwargs):
        """Get lists.

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
            With the default response processor, the list resources.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request("get", "lists", **kwargs)

    @handle_resp_proc(payload_filter())
    @handle_pagination
    def people(self, id, **kwargs):
        """Get people in a list.

        Parameters
        ----------
        id : int
            The list ID.
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

        return self.session.make_request("get", f"lists/{id}/people", **kwargs)

    @handle_resp_proc(resp_bool)
    def add(self, list, **kwargs):
        """Add list.

        Parameters
        ----------
        list : dict
            List representation.
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

        payload = {"list": list}

        return self.session.make_request("post", "lists", payload, **kwargs)

    @handle_resp_proc(resp_bool, resource_name="people_ids")
    def add_people(self, id, people_ids, **kwargs):
        """Add people to a list.

        Parameters
        ----------
        id : int
            The list ID.
        people_ids : list of int
            List of up to 100,000 person ``id``s.
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

        payload = {"people_ids": people_ids}

        return self.session.make_request(
            "post", f"lists/{id}/people", payload, **kwargs
        )

    @handle_resp_proc(resp_bool)
    def tag(self, id, tag, **kwargs):
        """Add a tag to all people in a list.

        Parameters
        ----------
        id : int
            The list ID.
        tag : str
            The tag name.
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

        return self.session.make_request("post", f"lists/{id}/tag/{tag}", **kwargs)

    @handle_resp_proc(payload_filter("id"), resource_name="export")
    def export(self, id, context="people", **kwargs):
        """Export list.

        Parameters
        ----------
        id : int
            The list ID.
        context : {"people", "households"}, optional
            Export data context.
        **kwargs
            Keyword arguments passed to ``NationBuilderClient.make_request``.
            `headers` will update the session level `headers` while `timeout` overrides
            the session default (see "Other Parameters") - anything else becomes a query
            parameter.

        Other Parameters
        ----------------
        resp_proc : callable
            Response processor (default extracts the export's ID for further querying:
            `payload_filter('id')`).
        headers : dict
            Add to or override the session level `headers`.
        timeout : int
            Override the session level request `timeout`.

        Returns
        -------
        int
            With the default response processor, the export's ID.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        payload = {"export": {"context": context}}

        return self.session.make_request(
            "post", f"lists/{id}/exports", payload, **kwargs
        )

    @handle_resp_proc(resp_bool)
    def update(self, id, list, **kwargs):
        """Update list.

        Parameters
        ----------
        id : int
            The list ID.
        list : dict
            List representation.
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

        payload = {"list": list}

        return self.session.make_request("put", f"lists/{id}", payload, **kwargs)

    @handle_resp_proc(resp_bool)
    def remove(self, id, **kwargs):
        """Remove list.

        Parameters
        ----------
        id : int
            The list ID.
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

        return self.session.make_request("delete", f"lists/{id}", **kwargs)

    @handle_resp_proc(resp_bool, resource_name="people_ids")
    def remove_people(self, id, people_ids, **kwargs):
        """Remove people from a list.

        Parameters
        ----------
        id : int
            The list ID.
        people_ids : list of int
            List of up to 100,000 person ``id``s.
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

        payload = {"people_ids": people_ids}

        return self.session.make_request(
            "delete", f"lists/{id}/people", payload, **kwargs
        )

    @handle_resp_proc(resp_bool)
    def remove_tag(self, id, tag, **kwargs):
        """Remove a tag from all people in a list.

        Parameters
        ----------
        id : int
            The list ID.
        tag : str
            The tag name.
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

        return self.session.make_request("delete", f"lists/{id}/tag/{tag}", **kwargs)
