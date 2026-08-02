"""OpenAPI schema helpers for drf-spectacular."""


def clean_caret_router_paths(endpoints):
    """
    Strip legacy '^' characters from router prefixes.

    Viewsets are registered with prefix '^' so detail URLs keep '/{pk}' when
    included under a path without a trailing slash. Spectacular would otherwise
    see paths like '/api/v1/accounts^/{id}/' and drop them.
    """
    return [
        (path.replace('^', ''), path_regex, method, callback)
        for path, path_regex, method, callback in endpoints
    ]
