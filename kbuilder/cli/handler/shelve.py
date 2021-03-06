"""Handlers for persistent storage."""
import shelve
from pathlib import Path

from cement.core.handler import CementBaseHandler

from kbuilder.cli.interface.database import IDatabase


class ShelveHandler(CementBaseHandler):
    """Handler for working with shelve."""
    class Meta:
        """Cement handler meta information."""
        interface = IDatabase
        label = 'shelve_handler'
        description = 'Store and retrieve objects'
        config_defaults = dict(
                foo='bar'
        )

    my_var = 'This is my var'

    def __init__(self):
        super().__init__()
        self.app = None
        self.local_root = None

    def _setup(self, app):
        self.app = app
        self.local_root = app.active_kernel.root

    def __setitem__(self, key: str, value: object) -> object:
        """Store an item in a data base.

        Args:
            key: the key to use to retrieve the item
            item: The item to store.

            Returns: n/a
        """
        with shelve.open(self._local_entry_path(key).as_posix()) as db:
            db[key] = value

    def __getitem__(self, key) -> object:
        """Store an item in a data base.

        Args:
            key: The key to use in getting the item.

            Returns:
                The object at the corresponding key
        """
        with shelve.open(self._local_entry_path(key).as_posix()) as db:
            return db[key]

    def _local_entry_path(self, key: str) -> Path:
        return self.local_root / '.kbuilder' / '{}.db'.format(key)
