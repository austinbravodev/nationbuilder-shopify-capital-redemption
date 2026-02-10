"""Generates `endpoints` list for `session.py` import and `NationBuilderClient`
attribute assignment.
"""

import importlib.util
import os
from functools import partialmethod


class Endpoint:
    """NationBuilder API endpoint base class.

    Defines a constructor that binds a `NationBuilderClient` instance.

    Attributes
    ----------
    session : NationBuilderClient
        The session the endpoint is bound to.

    Methods
    -------
    set_args(**kwargs)
        Set arguments common to all endpoint methods using `functools.partialmethod
        <https://docs.python.org/3/library/functools.html#functools.partialmethod>_`.
        Frozen arguments can be overriden by *keyword* arguments on method invocation.
    """

    def __init__(self, session):
        self.session = session

    @classmethod
    def set_args(cls, **kwargs):
        """Set arguments common to all endpoint methods using
        `functools.partialmethod
        <https://docs.python.org/3/library/functools.html#functools.partialmethod>_`.
        Frozen arguments can be overriden by *keyword* arguments on method invocation.
        """

        for meth_name, meth in cls.__dict__.items():
            if callable(meth):
                setattr(cls, meth_name, partialmethod(meth, **kwargs))


endpoints = []


with os.scandir("nationbuilder_api/endpoints/classes") as folder:
    for file in folder:
        if file.name.endswith(".py"):
            mod_name = file.name[:-3]
            spec = importlib.util.spec_from_file_location(mod_name, file.path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)

            for name in dir(mod):
                attr = getattr(mod, name)
                if (
                    isinstance(attr, type)
                    and issubclass(attr, Endpoint)
                    and attr is not Endpoint
                ):
                    endpoints.append((mod_name, attr))
