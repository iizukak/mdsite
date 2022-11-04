import argparse
import os
import dataclasses
import pkg_resources
import yaml

CONFIG_FILE_NAME = "potage.yaml"


@dataclasses.dataclass
class MarkDownFile:
    path: str
    title: str
    created_at: str
    edited_at: str


def parse_command_line_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="potage: Minimal Static Site Generator."
    )
    parser.add_argument("--version", action="store_true", help="Show potage version.")
    args = parser.parse_args()
    return args


def print_version():
    version = pkg_resources.get_distribution("potage").version
    print("potage version: " + version)


def parse_config() -> dict:
    with open(CONFIG_FILE_NAME) as file:
        config = yaml.safe_load(file)
    return config


def load_template():
    # Load jinja2 template files.
    # index.html is a main page template of the site.
    # pages.html is a general page template.
    pass


def load_markdown_files(input_dir):
    # Load files include input_dir recursively.
    # Retuen a list of MarkDown instances.
    pass


def convert_index(markdown):
    # Convert index.md's MarkDown instance to index.html.
    pass


def convert_page(markdown):
    # Convert a MarkDown instance into page.html
    pass


def main():
    args = parse_command_line_args()
    if args.version == True:
        print_version()
    else:
        print("Convert All MarkDown files")
        config = parse_config()
        print(config)
