import argparse
import os
import dataclasses

@dataclasses.dataclass
class Config:
    title: str
    author: str
    input_dir: str
    output_dir: str
    date_format: str

@dataclasses.dataclass
class MarkDownFile:
    path: str
    title: str
    created_at: str
    edited_at: str

def parse_command_line_args():
    # Parse potage command's arguments.
    # no argument: Try to convert all MarkDown files.
    # --version argument: Show potage package version.
    # --help argument: Show usage.
    pass

def parse_config(path):
    # Parse potage.yaml and return Config dataclass.
    # If some of the options are missing, raise a exception.
    # To check required parameters, please read Config dataclass definition.
    pass

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
    print("Hello, potage!")