"""Defines a NationBuilder API **People** interface."""

from nationbuilder_api.endpoints import Endpoint
from nationbuilder_api.endpoints.decorators import handle_pagination, handle_resp_proc
from nationbuilder_api.resp_procs import payload_filter, resource_eq, resp_bool


class People(Endpoint):
    """NationBuilder API **People** Interface

    Methods
    -------
    __call__(**kwargs)
        Get people.
    get(id=None, email=None, **kwargs)
        Get person by ID or email - if both are provided, ID is used.
    search(**kwargs)
        Search for people.
    near(location, **kwargs)
        Search for people near a given location.
    register(id, **kwargs)
        Sends account activation email.
    tags(id, **kwargs)
        Get a person's tags.
    contacts(id, **kwargs)
        Get a person's received contacts.
    memberships(id, **kwargs)
        Get a person's memberships.
    capital(id, **kwargs)
        Get a person's capital.
    count(**kwargs)
        Get the total number of people in the nation.
    me(**kwargs)
        Get the access token owner's representation.
    add(person, **kwargs)
        Add person. Use `update` for cases where the person may already exist.
    add_contact(id, contact, **kwargs)
        Add received contact to a person.
    add_membership(id, membership, **kwargs)
        Add membership to a person.
    add_capital(id, capital, **kwargs)
        Add capital to a person.
    note(id, content, **kwargs)
        Add note for a person.
    update(person, id=None, overwrite_if_add=False, **kwargs)
        Update (or add, see **Parameters** -> `id`) person. To avoid overwriting data,
        do not provide `id`, set `overwrite_if_add` to ``False``, and make sure one of
        `civicrm_id`, `county_file_id`, `dw_id`, `external_id`, `email`,
        `facebook_username`, `ngp_id`, `salesforce_id`, `twitter_login`, `van_id` is
        provided in the `payload`.
    add_tags(id, tag, **kwargs)
        Add tag(s) to a person.
    update_membership(id, membership, **kwargs)
        Updates a person's membership.
    remove(id, **kwargs)
        Remove person.
    remove_tags(id, tag, **kwargs)
        Remove tag(s) from a person.
    remove_membership(id, membership_name, **kwargs)
        Remove a person's membership.
    remove_capital(id, capital_id, **kwargs)
        Remove a single capital resource from a person.
    """

    resource_name = "person"

    @handle_resp_proc(payload_filter())
    @handle_pagination
    def __call__(self, **kwargs):
        """Get people.

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
            With the default response processor, the abbreviated person resources.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request("get", "people", **kwargs)

    @handle_resp_proc(payload_filter())
    def get(self, id=None, email=None, **kwargs):
        """Get person by ID or email - if both are provided, ID is used.

        Parameters
        ----------
        id : int, optional
            The person ID (default is ``None``).
        email : str, optional
            The person's email address (default is ``None``).
        **kwargs
            Keyword arguments passed to ``NationBuilderClient.make_request``.
            `headers` will update the session level `headers` while `timeout` overrides
            the session default (see "Other Parameters") - anything else becomes a query
            parameter.

        Other Parameters
        ----------------
        id_type : str
            If specifying ID, the ID type to use (e.g. `external`).
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
            With the default response processor, the person resource.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request(
            "get", f"people/{id if id else 'match?email=' + email}", **kwargs
        )

    @handle_resp_proc(payload_filter())
    @handle_pagination
    def search(self, **kwargs):
        """Search for people.

        Parameters
        ----------
        **kwargs
            Keyword arguments passed to ``NationBuilderClient.make_request``.
            `headers` will update the session level `headers` while `timeout` overrides
            the session default (see "Other Parameters") - anything else becomes a query
            parameter. See "Other Parameters" for searchable attributes.

        Other Parameters
        ----------------
        first_name, last_name, city, state, sex, civicrm_id, county_file_id,
        datatrust_id, dw_id, external_id, media_market_id, ngp_id, pf_strat_id, rnc_id,
        rnc_regid, salesforce_id, state_file_id, van_id : str
            Person attributes to match.
        birthdate : str
            Date in ``YYYY-MM-DD`` format.
        updated_since : str
            Datetime in ``ISO 8601`` format (``YYYY-MM-DDThh:mm:ss+/-hh:mm``).
        with_mobile : bool
            Whether the person has a mobile phone number.
        custom_values[<field_slug>]
            A mapping of Custom People Field slugs to values.
        membership_level_id : int
            A membership ID.
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

        return self.session.make_request("get", "people/search", **kwargs)

    @handle_resp_proc(payload_filter())
    @handle_pagination
    def near(self, location, **kwargs):
        """Search for people near a given location.

        Parameters
        ----------
        location : tuple of float
            Latitude and longitude coordinates.
        **kwargs
            Keyword arguments passed to ``NationBuilderClient.make_request``.
            `headers` will update the session level `headers` while `timeout` overrides
            the session default (see "Other Parameters") - anything else becomes a query
            parameter.

        Other Parameters
        ----------------
        distance : int
            Search radius in miles (if not given, NationBuilder sets the default server-
            side to ``1``).
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
            With the default response processor, the person resources.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        payload = {"results": {"location": location}}

        return self.session.make_request(
            "get", f"people/nearby?location={','.join(location)}", payload, **kwargs
        )

    @handle_resp_proc(resource_eq("success"), resource_name="status")
    def register(self, id, **kwargs):
        """Sends account activation email.

        Parameters
        ----------
        id : int
            The person ID.
        **kwargs
            Keyword arguments passed to ``NationBuilderClient.make_request``.
            `headers` will update the session level `headers` while `timeout` overrides
            the session default (see "Other Parameters") - anything else becomes a query
            parameter.

        Other Parameters
        ----------------
        resp_proc : callable
            Response processor (default indicates whether the email was successfully
            sent: `resource_eq('success')`).
        headers : dict
            Add to or override the session level `headers`.
        timeout : int
            Override the session level request `timeout`.

        Returns
        -------
        bool
            With the default response processor, the email's *sent* status.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request("get", f"people/{id}/register", **kwargs)

    @handle_resp_proc(payload_filter("tags"), resource_name="taggings")
    def tags(self, id, **kwargs):
        """Get a person's tags.

        Parameters
        ----------
        id : int
            The person ID.
        **kwargs
            Keyword arguments passed to ``NationBuilderClient.make_request``.
            `headers` will update the session level `headers` while `timeout` overrides
            the session default (see "Other Parameters") - anything else becomes a query
            parameter.

        Other Parameters
        ----------------
        resp_proc : callable
            Response processor (default extracts and filters the resources from the
            response: `payload_filter('tags')`).
        headers : dict
            Add to or override the session level `headers`.
        timeout : int
            Override the session level request `timeout`.

        Returns
        -------
        list of str
            With the default response processor, the tag names.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request("get", f"people/{id}/taggings", **kwargs)

    @handle_resp_proc(payload_filter())
    @handle_pagination
    def contacts(self, id, **kwargs):
        """Get a person's received contacts.

        Parameters
        ----------
        id : int
            The person ID.
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
            With the default response processor, the contact resources.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request("get", f"people/{id}/contacts", **kwargs)

    @handle_resp_proc(payload_filter())
    @handle_pagination
    def memberships(self, id, **kwargs):
        """Get a person's memberships.

        Parameters
        ----------
        id : int
            The person ID.
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
            With the default response processor, the membership resources.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request("get", f"people/{id}/memberships", **kwargs)

    @handle_resp_proc(payload_filter())
    @handle_pagination
    def capital(self, id, **kwargs):
        """Get a person's capital.

        Parameters
        ----------
        id : int
            The person ID.
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
            With the default response processor, the capital resources.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request("get", f"people/{id}/capitals", **kwargs)

    @handle_resp_proc(payload_filter(), resource_name="people_count")
    def count(self, **kwargs):
        """Get the total number of people in the nation.

        Parameters
        ----------
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
        int
            With the default response processor, the total number of people.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request("get", "people/count", **kwargs)

    @handle_resp_proc(payload_filter())
    def me(self, **kwargs):
        """Get the access token owner's representation.

        Parameters
        ----------
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
            With the default response processor, the person resource.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request("get", "people/me", **kwargs)

    @handle_resp_proc(resp_bool)
    def add(self, person, **kwargs):
        """Add person. Use `update` for cases where the person may already exist.

        Parameters
        ----------
        person : dict
            Person representation.
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

        payload = {"person": person}

        return self.session.make_request("post", "people", payload, **kwargs)

    @handle_resp_proc(resp_bool, resource_name="contact")
    def add_contact(self, id, contact, **kwargs):
        """Add received contact to a person.

        Parameters
        ----------
        id : int
            The person ID.
        contact : dict
            Contact representation.
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

        payload = {"contact": contact}

        return self.session.make_request(
            "post", f"people/{id}/contacts", payload, **kwargs
        )

    @handle_resp_proc(resp_bool, resource_name="membership")
    def add_membership(self, id, membership, **kwargs):
        """Add membership to a person.

        Parameters
        ----------
        id : int
            The person ID.
        membership : dict
            Membership representation.
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

        payload = {"membership": membership}

        return self.session.make_request(
            "post", f"people/{id}/memberships", payload, **kwargs
        )

    @handle_resp_proc(resp_bool, resource_name="capital")
    def add_capital(self, id, capital, **kwargs):
        """Add capital to a person.

        Parameters
        ----------
        id : int
            The person ID.
        capital : dict
            Capital representation.
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

        payload = {"capital": capital}

        return self.session.make_request(
            "post", f"people/{id}/capitals", payload, **kwargs
        )

    @handle_resp_proc(resp_bool, resource_name="note")
    def note(self, id, content, **kwargs):
        """Add note for a person.

        Parameters
        ----------
        id : int
            The person ID.
        content : str
            The note's content.
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

        payload = {"note": {"content": content}}

        return self.session.make_request(
            "post", f"people/{id}/notes", payload, **kwargs
        )

    @handle_resp_proc(resp_bool)
    def update(self, person, id=None, overwrite_if_add=False, **kwargs):
        """Update (or add, see **Parameters** -> `id`) person. To avoid overwriting data,
        do not provide `id`, set `overwrite_if_add` to ``False``, and make sure one of
        `civicrm_id`, `county_file_id`, `dw_id`, `external_id`, `email`,
        `facebook_username`, `ngp_id`, `salesforce_id`, `twitter_login`, `van_id` is
        provided in the `payload`.

        Parameters
        ----------
        person : dict
            Person representation.
        id : int, optional
            The person ID (default is ``None``). If not provided, a person will be
            created if they don't exist.
        overwrite_if_add : bool, optional
            If `id` is not provided, whether to overwrite data (default is ``True``).
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

        payload = {"person": person}

        return self.session.make_request(
            "put",
            f"people/{id if id else ('push' if overwrite_if_add else 'add')}",
            payload,
            **kwargs,
        )

    @handle_resp_proc(resp_bool, resource_name="tagging")
    def add_tags(self, id, tag, **kwargs):
        """Add tag(s) to a person.

        Parameters
        ----------
        id : int
            The person ID.
        tag : list of str or str
            Tag name(s). ``str`` represents a single tag.
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

        payload = {"tagging": {"tag": tag}}

        return self.session.make_request(
            "put", f"people/{id}/taggings", payload, **kwargs
        )

    @handle_resp_proc(resp_bool, resource_name="membership")
    def update_membership(self, id, membership, **kwargs):
        """Updates a person's membership.

        Parameters
        ----------
        id : int
            The person ID.
        membership : dict
            Membership representation.
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

        payload = {"membership": membership}

        return self.session.make_request(
            "put", f"people/{id}/memberships", payload, **kwargs
        )

    @handle_resp_proc(resp_bool)
    def remove(self, id, **kwargs):
        """Remove person.

        Parameters
        ----------
        id : int
            The person ID.
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

        return self.session.make_request("delete", f"people/{id}", **kwargs)

    @handle_resp_proc(resp_bool, resource_name="tagging")
    def remove_tags(self, id, tag, **kwargs):
        """Remove tag(s) from a person.

        Parameters
        ----------
        id : int
            The person ID.
        tag : list of str or str
            Tag name(s). ``str`` represents a single tag.
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

        payload = {"tagging": {"tag": tag}}

        return self.session.make_request(
            "delete", f"people/{id}/taggings", payload, **kwargs
        )

    @handle_resp_proc(resp_bool)
    def remove_membership(self, id, membership_name, **kwargs):
        """Remove a person's membership.

        Parameters
        ----------
        id : int
            The person ID.
        membership_name : str
            The membership name.
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

        return self.session.make_request(
            "delete", f"people/{id}/memberships/{membership_name}", **kwargs
        )

    @handle_resp_proc(resp_bool)
    def remove_capital(self, id, capital_id, **kwargs):
        """Remove a single capital resource from a person.

        Parameters
        ----------
        id : int
            The person ID.
        capital_id : int
            The capital ID.
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

        return self.session.make_request(
            "delete", f"people/{id}/capital/{capital_id}", **kwargs
        )
