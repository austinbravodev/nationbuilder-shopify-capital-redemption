"""Defines helper functions for implicit use with endpoints.

Functions
---------
handle_filter(resource, filter)
    Handle multiple and / or nested resource filter attributes.
filter_resource(resource, filter)
    Filter resource for single attribute or delegate to `handle_filter`.
handle_resp_proc_args(resp_proc, resp_proc_args)
    If the response processor takes additional arguments, freeze them.
proc_resp(resp, resp_proc, resp_proc_args)
    Handle one or more response processors.
"""

from functools import partial


def handle_resp_proc_args(resp_proc, resp_proc_args):
    """If the response processor takes additional arguments, freeze them."""

    if resp_proc_args:
        resp_proc_arg_keys = resp_proc_args.keys()
        if hasattr(resp_proc, "keywords"):
            resp_proc_arg_keys -= resp_proc.keywords.keys()

        try:
            resp_proc_meta = resp_proc.__code__
        except AttributeError:
            resp_proc_meta = resp_proc.func.__code__

        args_to_freeze = (
            resp_proc_arg_keys
            & resp_proc_meta.co_varnames[1 : resp_proc_meta.co_argcount]
        )

        return partial(
            resp_proc, **{arg: resp_proc_args[arg] for arg in args_to_freeze}
        )

    return resp_proc


def proc_resp(resp, resp_proc, resp_proc_args):
    """Handle one or more response processors."""

    handle_resp_proc_args_partial = partial(
        handle_resp_proc_args, resp_proc_args=resp_proc_args
    )

    if callable(resp_proc):
        return handle_resp_proc_args_partial(resp_proc)(resp)

    for rp in resp_proc:
        resp = handle_resp_proc_args_partial(rp)(resp)

    return resp
