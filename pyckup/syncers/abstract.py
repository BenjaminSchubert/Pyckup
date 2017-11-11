from abc import abstractmethod
from configparser import NoOptionError
import datetime
import os
import subprocess

from pyckup.exceptions import InvalidConfigException


class AbstractSyncer:
    current_backup_relative_path = "./current"

    start_date = None

    @property
    def temporary_backup_directory(self):
        return os.path.join(self.destination, "incomplete")

    def __init__(self, config, section):
        try:
            self.source = config.get(section, "source")
            self.destination = config.get(section, "destination")

            self.date_format = config.get(section, "date_format", fallback="%Y.%m.%d-%H-%M-%S", raw=True)
            self.exclude = config.get(section, "exclude", fallback="")
        except NoOptionError as exc:
            raise InvalidConfigException(exc.message)

    def get_command(self):
        return [
            "rsync",
            "-aAXH",
            "--link-dest", self.current_backup_relative_path,
            " ".join(["--exclude='{}'".format(excluded.strip()) for excluded in self.exclude.split(",")]),
            self.source + "/",
            self.temporary_backup_directory
        ]

    @abstractmethod
    def pre_sync(self):
        """Prepare for syncing."""

    @abstractmethod
    def post_sync(self):
        """Cleanup after sync."""

    def sync(self):
        # FIXME: check that rsync is installed
        try:
            subprocess.check_call(self.get_command())
        except subprocess.CalledProcessError as exc:
            raise exc

    def __call__(self):
        self.start_date = datetime.datetime.now().strftime(self.date_format)
        self.pre_sync()
        self.sync()
        self.post_sync()
