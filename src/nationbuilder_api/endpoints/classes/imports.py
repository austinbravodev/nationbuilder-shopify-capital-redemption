"""Defines a NationBuilder API **Imports** interface."""

from nationbuilder_api.endpoints import Endpoint
from nationbuilder_api.endpoints.decorators import handle_resp_proc
from nationbuilder_api.resp_procs import payload_filter


class Imports(Endpoint):
    """NationBuilder API **Imports** Interface

    Methods
    -------
    get(id, **kwargs)
        Get import.
    result(id, **kwargs)
        Get import results.
    add(file, type="people", is_overwritable=False, **kwargs)
        Import people or voting history. Each import must be 50 MB or less.
    """

    resource_name = "import"

    @handle_resp_proc(payload_filter([("status", ["name"])]))
    def get(self, id, **kwargs):
        """Get import.

        Parameters
        ----------
        id : int
            The import ID.
        **kwargs
            Keyword arguments passed to ``NationBuilderClient.make_request``.
            `headers` will update the session level `headers` while `timeout` overrides
            the session default (see "Other Parameters") - anything else becomes a query
            parameter.

        Other Parameters
        ----------------
        resp_proc : callable
            Response processor (default extracts and filters the resource from the
            response: `payload_filter([('status', ['name'])])`).
        headers : dict
            Add to or override the session level `headers`.
        timeout : int
            Override the session level request `timeout`.

        Returns
        -------
        str
            With the default response processor, the import's status.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request("get", f"imports/{id}", **kwargs)

    @handle_resp_proc(payload_filter(), resource_name="result")
    def result(self, id, **kwargs):
        """Get import results.

        Parameters
        ----------
        id : int
            The import ID.
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
            With the default response processor, the import's results.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request("get", f"imports/{id}/result", **kwargs)

    @handle_resp_proc(payload_filter("id"))
    def add(self, file, type="people", is_overwritable=False, **kwargs):
        """Import people or voting history. Each import must be 50 MB or less.

        Parameters
        ----------
        file : str
            A Base64 encoded CSV file (50 MB or less).
        type : {"people", "ballot"}, optional
            The import type.
        is_overwritable : bool, optional
            Whether to overwrite existing data.
        **kwargs
            Keyword arguments passed to ``NationBuilderClient.make_request``.
            `headers` will update the session level `headers` while `timeout` overrides
            the session default (see "Other Parameters") - anything else becomes a query
            parameter.

        Other Parameters
        ----------------
        resp_proc : callable
            Response processor (default extracts the import ID for further querying:
            `payload_filter('id')`).
        headers : dict
            Add to or override the session level `headers`.
        timeout : int
            Override the session level request `timeout`.

        Returns
        -------
        int
            With the default response processor, the import ID.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        payload = {
            "import": {"file": file, "type": type, "is_overwritable": is_overwritable}
        }

        return self.session.make_request("post", "imports", payload, **kwargs)
