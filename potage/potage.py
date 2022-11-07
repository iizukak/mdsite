import argparse
import os
import dataclasses
from pathlib import Path, PurePath
from site import execsitecustomize
import yaml
import importlib
from importlib.metadata import version
import importlib.resources
import pprint

CONFIG_FILE_NAME = "potage.yaml"
INDEX_HTML_FILE_NAME = "index.html"
PAGE_HTML_FILE_NAME = "page.html"


@dataclasses.dataclass
class MarkDownFile:
    path: Path
    output_path: Path
    output_dir: Path
    created_at: str
    edited_at: str
    contents: str


def parse_command_line_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="potage: Minimal Static Site Generator."
    )
    parser.add_argument("--version", action="store_true", help="Show potage version.")
    args = parser.parse_args()
    return args


def print_version():
    v = version("potage")
    print("potage version: " + v)


def parse_config() -> dict:
    with open(CONFIG_FILE_NAME) as file:
        config = yaml.safe_load(file)
    print("load settings...")
    pprint.pprint(config)
    print()
    return config


def load_template() -> tuple[str, str]:
    # Load jinja2 template files.
    # index.html is a main page template of the site.
    # pages.html is a general page template.
    pkg = importlib.resources.files("potage")
    index_template_path = pkg / "template" / "index.html"
    page_template_path = pkg / "template" / "pages.html"
    index_template = index_template_path.read_text()
    page_template = page_template_path.read_text()
    return index_template, page_template


def load_markdown_files(config: dict) -> list[MarkDownFile]:
    # Load .md files in input_dir, recursively.
    # Retuen a list of MarkDown instances.
    print("collecting target markdown files...")
    markdowns = []
    input_paths = Path(config["input_dir"]).glob("**/*.md")
    for path in input_paths:
        print(path)
        output_dir = Path(config["output_dir"], *path.parts[1:-1])
        output_html_file_name = path.stem + ".html"
        output_path = Path(output_dir, output_html_file_name)
        stat = os.stat(path)
        with open(path) as f:
            contents = f.read()
        markdown = MarkDownFile(
            path=path,
            output_path=output_path,
            output_dir=output_dir,
            created_at=stat.st_birthtime,
            edited_at=stat.st_mtime,
            contents=contents,
        )
        markdowns.append(markdown)
    print()
    return markdowns


def make_output_dirs(markdowns: list[MarkDownFile]):
    # mkdir recursively
    # input: in/foo/bar -> mkdir: out/foo/bar
    for markdown in markdowns:
        os.makedirs(markdown.output_dir, exist_ok=True)


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
        config = parse_config()
        index_template, page_template = load_template()
        markdown_files = load_markdown_files(config)
        make_output_dirs(markdown_files)
