from typing import Optional

from cloudisk.tools.scope import Scope


class Context:
    def __init__(self, scopes: Optional[dict[str, Scope] | list[Scope]]):  # noqa: D107
        if scopes is None:
            scopes = {}

        if isinstance(scopes, list):
            scopes = {scope.name: scope for scope in scopes}

        self.scopes = scopes

    def __getattr__(self, name: str):  # noqa: D105
        return self.scopes.get(name)

    def add_scope(self, scope: Scope):
        self.scopes[scope.name] = scope

    def drop_scope(self, name: str):
        del self.scope[name]
