class Router:
    def __init__(self) -> None:
        self.routes = {}

    def add_route(self, method, path, handler):
        self.routes[(method, path)] = handler

    def get(self, path):
        def decorator(fn):
            self.add_route("GET", path, fn)
            return

        return decorator

    def post(self, path):
        def decorator(fn):
            self.add_route("POST", path, fn)
            return

        return decorator
