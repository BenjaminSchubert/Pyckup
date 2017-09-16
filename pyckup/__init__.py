#!/usr/bin/env python3

import argparse
from configparser import ConfigParser
import sys

from pyckup.exceptions import InvalidConfigException, PyckupException
from pyckup.syncers import LocalSyncer


__author__ = "Benjamin Schubert <ben.c.schubert@gmail.com>"


DEFAULT_CONFIGURATION_PATHS = [".pyckup.conf", "~/.pyckup.conf", "/etc/pyckup.conf"]


def parse_args(args=sys.argv[1:]):
    parser = argparse.ArgumentParser(description="Pyckup, backup made simple")
    parser.add_argument(
        "-c", "--config", type=str,
        help="Configuration file. If not given, will look for {} in this order".format(
            ", ".join(DEFAULT_CONFIGURATION_PATHS)
        )
    )

    parser.add_argument(
        "-f", "--force", action="store_true", help="Run valid backups even if others have errors."
    )

    parser.add_argument(
        "profile", type=str, nargs="*",
        help="The name of the profile(s) to execute. By default will run all profiles found in the configuration"
    )

    parsed_args = parser.parse_args(args)

    if parsed_args.config is not None:
        if not os.path.exists(parsed_args.config):
            logger.error("Could not find {}".format(parsed_args.config))
            exit(1)

    return vars(parsed_args)


def parse_config(config_file):
    config = ConfigParser()

    if config_file is not None:
        config.read(config_file)
    else:
        for file_ in DEFAULT_CONFIGURATION_PATHS:
            config.read(file_)

    if not config.sections():
        raise InvalidConfigException("No profile defined.")
    
    return config


def get_syncer(config, section):
    return LocalSyncer(config, section)


def main():
    try:
        arguments = parse_args()
        config = parse_config(arguments["config"])

        for section in arguments["profile"] or config.sections():
            syncer = get_syncer(config, section)
            syncer()
    except PyckupException as exc:
        print(exc)
        exit(1)
