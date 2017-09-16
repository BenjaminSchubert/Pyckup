from contextlib import suppress
import os
import shutil

from .abstract import AbstractSyncer
from pyckup.exceptions import SyncException


class LocalSyncer(AbstractSyncer):
    @property
    def current_backup(self):
        return os.path.join(self.destination, "current")

    def pre_sync(self):
        try:
            os.makedirs(self.destination, exist_ok=True)
        except PermissionError as exc:
            raise SyncException("Could not create destination directory, got: {}".format(exc))

        try:
            with suppress(FileNotFoundError):
                shutil.rmtree(os.path.join(self.destination, "incomplete"))
        except PermissionError as exc:
            raise SyncException("Could not remove previous failed run, got: {}".format(exc))

    def post_sync(self):
        os.rename(
            os.path.join(self.destination, "incomplete"),
            os.path.join(self.destination, self.start_date)
        )

        os.symlink(os.path.join(self.destination, self.start_date), os.path.join(self.destination, "next-current"))
        os.rename(os.path.join(self.destination, "next-current"), os.path.join(self.destination, "current"))
