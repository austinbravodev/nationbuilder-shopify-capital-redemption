"""Defines endpoint method decorators.

Functions
---------
handle_pagination
    Paginate through responses.
handle_resp_proc(**resp_proc_args)
    Handle response processing.
"""

from functools import partial, wraps
from urllib.parse import parse_qs, urlparse

from .helpers import proc_resp

MAX_RESPS_NAME = "max_resps"
RESP_PROC_NAME = "resp_proc"
RESOURCE_NAME = "resource_name"

RESP_PROC_ARGS = {
    RESOURCE_NAME,
}


def handle_pagination(f):
    """Paginate through responses."""

    @wraps(f)
    def dec_f(self, *args, **kwargs):
        yield_resps = kwargs.pop("yield_resps", False)

        if not yield_resps:
            max_resps = kwargs.pop(MAX_RESPS_NAME, -1)
            resps = []

        try:
            while yield_resps or len(resps) != max_resps:
                resp = f(self, *args, **kwargs)

                if not yield_resps:
                    resps.append(resp)
                else:
                    yield resp

                next_page = resp.json().get("next")

                if next_page:
                    kwargs.update(parse_qs(urlparse(next_page).query))
                else:
                    break

        except Exception:

            if not yield_resps and resps:
                self.session.logger.exception(
                    "An error occured - a partial list of responses may be returned."
                )
            else:
                raise

        if not yield_resps:
            return resps

    dec_f.resource_name = "results"

    return dec_f


def handle_resp_proc(resp_proc_dflt=None, **resp_proc_args):
    """Handle response processing.

    If handling paginated responses, processed response results are flattened into a
    single list.

    Parameters
    ----------
    **resp_proc_args
        Optional keyword arguments passed to response processors. Overridden by
        arguments passed to the response processor.
    """

    def dec(f):
        @wraps(f)
        def dec_f(self, *args, **kwargs):
            resp_proc = kwargs.pop(RESP_PROC_NAME, resp_proc_dflt)
            res = f(self, *args, **kwargs)

            if resp_proc and res:

                for arg in RESP_PROC_ARGS - resp_proc_args.keys():
                    try:
                        resp_proc_args[arg] = getattr(f, arg, getattr(self, arg))
                    except AttributeError:
                        pass

                proc_resp_partial = partial(
                    proc_resp,
                    resp_proc=resp_proc,
                    resp_proc_args=resp_proc_args,
                )

                if isinstance(res, list):
                    if all(res):
                        resps = []
                        for resp in res:
                            resps += proc_resp_partial(resp)
                        return resps

                    self.session.logger.error(
                        "Not all requests were successful - unprocessed \
                        response(s) will be returned."
                    )
                    return res  # change this at some point

                return proc_resp_partial(res)

            return res

        return dec_f

    return dec
