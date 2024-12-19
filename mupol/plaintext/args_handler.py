import argparse
import configparser
import os

DEFAULT_CONFIG_FOLDER = "config"
DEFAULT_CONFIG = "config.ini"


class ArgsHandler:
    def __init__(self, args):
        self._parser = argparse.ArgumentParser(
            description="Problem generator and solver / optimization parser"
        )
        self._args = args
        self._setup_parser()

    def _setup_parser(self) -> None:
        self._parser.add_argument(
            "--config",
            type=str,
            help="Name of the configuration file",
            default=DEFAULT_CONFIG,
        )
        self._parser.add_argument(
            "--num-freighters", help="Number of freighters", type=int
        )
        self._parser.add_argument(
            "--min-num-trucks", help="Minimum number of trucks", type=int
        )
        self._parser.add_argument(
            "--max-num-trucks", help="Maximum number of trucks", type=int
        )
        self._parser.add_argument("--truck-capacity", help="Truck capacity", type=int)
        self._parser.add_argument("--num-orders", help="Number of orders", type=int)
        self._parser.add_argument(
            "--min-order-volume", help="Minimum order volume", type=int
        )
        self._parser.add_argument(
            "--max-order-volume", help="Maximum order volume", type=int
        )
        self._parser.add_argument("--random-seed", help="Random seed", type=int)
        self._parser.add_argument(
            "--num-iters", help="Number of iterations of optimizer", type=int
        )
        self.args = self._parser.parse_args(self._args)

        self._validate_config()
        self._config = configparser.ConfigParser()
        self._config.read(self._config_path)

        self._parser.set_defaults(**self._config["Problem parameters"])
        self._parser.set_defaults(**self._config["Solver parameters"])
        self.args = self._parser.parse_args(self._args)

    def _validate_config(self) -> None:
        self._given_config_path = os.path.join(
            os.getcwd(), DEFAULT_CONFIG_FOLDER, self.args.config
        )
        if not os.path.isfile(self._given_config_path):
            raise ValueError(f"Could not find config file at {self._given_config_path}")
        else:
            self._config_path = self._given_config_path
