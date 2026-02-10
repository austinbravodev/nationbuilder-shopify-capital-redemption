"""Defines response processors passed to endpoint methods.

Functions either take a ``requests.Response`` object or return a callable that does. If
a function returns a callable, it should be called when passed as argument. Else, pass
the function as object::

    # If function returns a callable:
    endpoint.method(..., resp_proc=func(...))

    # Else:
    endpoint.method(..., resp_proc=func)

Functions
---------
payload_filter(filter=None, resource_name=None)
    Extract and optionally filter the resource(s) from the response.
resource_eq(obj, filter=None, resource_name=None)
    Check the optionally filtered resource(s) for equivalency with some object.
check_for_status(*status)
    Check that the response status is present in the given status.
resp_bool(resp):
    Check that the request succeeded, else return the unmodified response.
"""

from functools import partial

from .helpers import filter_resource


def payload_filter(filter=None, resource_name=None):
    """Extract and optionally filter the resource(s) from the response.

    If the object extracted by `resource_name` is a ``list``, it is assumed to be a list
    of resources and each is filtered individually.

    Parameters
    ----------
    filter : str or list, optional
        Resource attributes to return (default is ``None``). To return multuple and / or
        nested attributes, use the following structure::

            [
                "attr",
                (
                    "attr_with_nested_attrs",
                    [
                        "nested_attr",
                        (
                            "nested_attr_with_nested_attrs",
                            [
                                "deep_attr_one",
                                "deep_attr_two"
                            ]
                        )
                    ]
                ),
                "attr_three"
            ]

    resource_name : str, optional
        The key of the object to extract from the response. If given, will override the
        implicitly provided argument.

    Returns
    -------
    func
        A function that returns the optionally filtered resource(s).
    """

    def f(resp, resource_name=None):
        payload = resp.json()
        resource = payload.get(resource_name, payload)

        if resource and filter:
            if isinstance(resource, list):
                filtered_resources = []
                for rsrc in resource:
                    filtered_resources.append(filter_resource(rsrc, filter))
                return filtered_resources

            return filter_resource(resource, filter)

        return resource

    if resource_name:
        f = partial(f, resource_name=resource_name)

    return f


def resource_eq(obj, filter=None, resource_name=None):
    """Check the optionally filtered resource(s) for equivalency with some object.

    Parameters
    ----------
    obj
        The object to match.
    filter : str or list, optional
        Resource attributes to compare (default is ``None``). To compare multuple and /
        or nested attributes, use the following structure::

            [
                "attr",
                (
                    "attr_with_nested_attrs",
                    [
                        "nested_attr",
                        (
                            "nested_attr_with_nested_attrs",
                            [
                                "deep_attr_one",
                                "deep_attr_two"
                            ]
                        )
                    ]
                ),
                "attr_three"
            ]

    resource_name : str, optional
        The key of the object to extract from the response. If given, will override the
        implicitly provided argument.

    Returns
    -------
    func
        A function that returns ``bool`` indicating equivalency.
    """

    def f(resp, resource_name=None):
        return payload_filter(filter)(resp, resource_name) == obj

    if resource_name:
        f = partial(f, resource_name=resource_name)

    return f


def check_for_status(*status):
    """Check that the response status is present in the given status.

    Parameters
    ----------
    status : int
        One or more status codes. If providing an iterable, make sure to unpack it.

    Returns
    -------
    func
        A function that returns ``bool`` indicating a match.
    """

    def f(resp):
        return resp.status_code in status

    return f


def resp_bool(resp):
    """Check that the request succeeded, else return the unmodified response.

    Returns
    -------
    True
        If the request succeeded.
    requests.Response
        The unmodified response on a bad request.
    """

    return bool(resp) or resp
