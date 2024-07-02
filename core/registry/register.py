from rich.table import Table
from rich.console import Console


class Registry:
    def __init__(self, name, location):
        self.name = name
        self.location = location
        self._registry = {}

    def register(self, name):
        """Decorator to register a new module under a given name."""
        def decorator(cls):
            if name in self._registry:
                raise KeyError(f"{name} is already registered in {self.name}")
            self._registry[name] = cls
            return cls
        return decorator

    def get(self, name):
        """Retrieve a registered module by name."""
        if name not in self._registry:
            raise KeyError(
                f"No module registered under name {name} in {self.name}")
        return self._registry[name]

    def __len__(self):
        """Return the number of registered modules."""
        return len(self._registry)

    def __repr__(self):
        """Represent the full registry as a table using the rich library."""
        table = Table(title=f"{self.name} Registry at {self.location}")
        table.add_column("Module Name", style="magenta")
        table.add_column("Module Class", style="cyan")
        for name, cls in self._registry.items():
            table.add_row(name, cls.__name__)
        console = Console()
        console.print(table)
        return f"{self.name} Registry with {len(self)} modules."

    @property
    def list_modules(self):
        """List all registered modules."""
        return list(self._registry.keys())