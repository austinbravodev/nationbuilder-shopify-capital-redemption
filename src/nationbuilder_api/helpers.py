"""Defines helper functions for implicit use throughout the library.

Functions
---------
handle_rate_limit
    Decorator for session request methods subject to the NationBuilder API's rate
    limiting.
"""


def has_level_handler(logger):
    """Check if there is a handler in the logging chain that will handle the
    given logger's :meth:`effective level <~logging.Logger.getEffectiveLevel>`.

    Credits
    -------
    Taken from `Flask's logging setup
    <https://github.com/pallets/flask/blob/master/src/flask/logging.py>`_
    """
    level = logger.getEffectiveLevel()
    current = logger

    while current:
        if any(handler.level <= level for handler in current.handlers):
            return True

        if not current.propagate:
            break

        current = current.parent

    return False


def handle_filter(resource, filter):
    """Handle multiple and / or nested resource filter attributes."""

    filtered_resource = {}
    for attr in filter:
        if isinstance(attr, str):
            filtered_resource[attr] = resource.get(attr)
        else:
            filtered_resource[attr[0]] = handle_filter(attr[1])(resource[attr[0]])

    return filtered_resource


def filter_resource(resource, filter):
    """Filter resource for single attribute or delegate to `handle_filter`."""

    if isinstance(filter, str):
        return resource.get(filter)

    return handle_filter(resource, filter)
