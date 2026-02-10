"""Defines a NationBuilder API **Exports** interface."""

from nationbuilder_api.endpoints import Endpoint
from nationbuilder_api.endpoints.decorators import handle_resp_proc
from nationbuilder_api.resp_procs import payload_filter, resp_bool


class Exports(Endpoint):
    """NationBuilder API **Exports** Interface

    Methods
    -------
    get(id, **kwargs)
        Get export.
    remove(id, **kwargs)
        Remove export.
    """

    resource_name = "export"

    @handle_resp_proc(payload_filter("download_url"))
    def get(self, id, **kwargs):
        """Get export.

        Parameters
        ----------
        id : int
            The export ID.
        **kwargs
            Keyword arguments passed to ``NationBuilderClient.make_request``.
            `headers` will update the session level `headers` while `timeout` overrides
            the session default (see "Other Parameters") - anything else becomes a query
            parameter.

        Other Parameters
        ----------------
        resp_proc : callable
            Response processor (default extracts and filters the resource from the
            response: `payload_filter('download_url')`).
        headers : dict
            Add to or override the session level `headers`.
        timeout : int
            Override the session level request `timeout`.

        Returns
        -------
        str
            With the default response processor, the export's location (download URL or
            ``None`` if incomplete).
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request("get", f"exports/{id}", **kwargs)

    @handle_resp_proc(resp_bool)
    def remove(self, id, **kwargs):
        """Remove export.

        Parameters
        ----------
        id : int
            The export ID.
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

        return self.session.make_request("delete", f"exports/{id}", **kwargs)
