"""Defines a NationBuilder API **Blog Posts** interface."""

from nationbuilder_api.endpoints import Endpoint
from nationbuilder_api.endpoints.decorators import handle_pagination, handle_resp_proc
from nationbuilder_api.resp_procs import payload_filter, resp_bool


class BlogPosts(Endpoint):
    """NationBuilder API **Blog Posts** Interface

    Methods
    -------
    __call__(site_slug, blog_id, **kwargs)
        Get blog posts.
    get(id, site_slug, blog_id, **kwargs)
        Get blog post.
    find(external_id, site_slug, blog_id, **kwargs)
        Get blog post by its external ID.
    add(blog_post, site_slug, blog_id, **kwargs)
        Add blog post.
    update(id, blog_post, site_slug, blog_id, **kwargs)
        Update blog post - partial updates are not supported.
    remove(id, site_slug, blog_id, **kwargs)
        Remove blog post.

    Notes
    -----
    This endpoint has 2 parameters common to all methods: `site_slug` and `blog_id`. Use
    `Endpoint.set_args` to freeze common default values.
    """

    resource_name = "blog_post"

    @handle_resp_proc(payload_filter())
    @handle_pagination
    def __call__(self, site_slug, blog_id, **kwargs):
        """Get blog posts.

        Parameters
        ----------
        site_slug : str
            The slug of the site containing the blog post(s). Common to all endpoint
            methods - use `Endpoint.set_args` to freeze a common default value.
        blog_id : int
            The ID of the blog containing the blog post(s). Common to all endpoint
            methods - use `Endpoint.set_args` to freeze a common default value.
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
            With the default response processor, the blog post resources.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request(
            "get", f"sites/{site_slug}/pages/blogs/{blog_id}/posts", **kwargs
        )

    @handle_resp_proc(payload_filter())
    def get(self, id, site_slug, blog_id, **kwargs):
        """Get blog post.

        Parameters
        ----------
        id : int
            The blog post ID.
        site_slug : str
            The slug of the site containing the blog post(s). Common to all endpoint
            methods - use `Endpoint.set_args` to freeze a common default value.
        blog_id : int
            The ID of the blog containing the blog post(s). Common to all endpoint
            methods - use `Endpoint.set_args` to freeze a common default value.
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
            With the default response processor, the blog post resource.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request(
            "get", f"sites/{site_slug}/pages/blogs/{blog_id}/posts/{id}", **kwargs
        )

    @handle_resp_proc(payload_filter(), resource_name="id")
    def find(self, external_id, site_slug, blog_id, **kwargs):
        """Get blog post by its external ID.

        Parameters
        ----------
        external_id : str or int
            The blog post's `external_id`.
        site_slug : str
            The slug of the site containing the blog post(s). Common to all endpoint
            methods - use `Endpoint.set_args` to freeze a common default value.
        blog_id : int
            The ID of the blog containing the blog post(s). Common to all endpoint
            methods - use `Endpoint.set_args` to freeze a common default value.
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
            With the default response processor, the ID of the matching blog post.
        requests.Response
            Without the default response processor, the unmodified response.
        """

        return self.session.make_request(
            "get",
            f"sites/{site_slug}/pages/blogs/{blog_id}/match?external_id={external_id}",
            **kwargs,
        )

    @handle_resp_proc(resp_bool)
    def add(self, blog_post, site_slug, blog_id, **kwargs):
        """Add blog post.

        Parameters
        ----------
        blog_post : dict
            Blog post representation.
        site_slug : str
            The slug of the site containing the blog post(s). Common to all endpoint
            methods - use `Endpoint.set_args` to freeze a common default value.
        blog_id : int
            The ID of the blog containing the blog post(s). Common to all endpoint
            methods - use `Endpoint.set_args` to freeze a common default value.
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

        payload = {"blog_post": blog_post}

        return self.session.make_request(
            "post", f"sites/{site_slug}/pages/blogs/{blog_id}/posts", payload, **kwargs
        )

    @handle_resp_proc(resp_bool)
    def update(self, id, blog_post, site_slug, blog_id, **kwargs):
        """Update blog post - partial updates are not supported.

        Parameters
        ----------
        id : int
            The blog post ID.
        blog_post : dict
            The *full* blog post representation - partial updates are not supported.
        site_slug : str
            The slug of the site containing the blog post(s). Common to all endpoint
            methods - use `Endpoint.set_args` to freeze a common default value.
        blog_id : int
            The ID of the blog containing the blog post(s). Common to all endpoint
            methods - use `Endpoint.set_args` to freeze a common default value.
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

        payload = {"blog_post": blog_post}

        return self.session.make_request(
            "put",
            f"sites/{site_slug}/pages/blogs/{blog_id}/posts/{id}",
            payload,
            **kwargs,
        )

    @handle_resp_proc(resp_bool)
    def remove(self, id, site_slug, blog_id, **kwargs):
        """Remove blog post.

        Parameters
        ----------
        id : int
            The blog post ID.
        site_slug : str
            The slug of the site containing the blog post(s). Common to all endpoint
            methods - use `Endpoint.set_args` to freeze a common default value.
        blog_id : int
            The ID of the blog containing the blog post(s). Common to all endpoint
            methods - use `Endpoint.set_args` to freeze a common default value.
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
            "delete", f"sites/{site_slug}/pages/blogs/{blog_id}/posts/{id}", **kwargs
        )
