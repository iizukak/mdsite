import argparse
import dataclasses
import importlib
import importlib.resources
import os
import pprint
import shutil
import platform
from datetime import date
from importlib.metadata import version
from pathlib import Path

import yaml
from jinja2 import Template
from markdown import markdown

css_file_name = "mdsite.css"


@dataclasses.dataclass
class MarkDownFile:
    path: Path
    output_path: Path
    output_dir: Path
    created_at: str
    edited_at: str
    contents: str
    title: str
    link: str
    link_to_root: str
    category: str


def parse_command_line_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="mdsite: Minimal Static Site Generator."
    )
    parser.add_argument("--version", action="store_true", help="Show mdsite version.")
    parser.add_argument("--config", help="Specify YAML file.", default="mdsite.yaml")
    args = parser.parse_args()
    return args


def print_version():
    v = version("mdsite")
    print("mdsite version: " + v)


def parse_config(config_file_name: str) -> dict:
    with open(config_file_name) as file:
        config = yaml.safe_load(file)
    print("load settings...")
    pprint.pprint(config)
    print()
    return config


def load_template() -> tuple[str, str, str]:
    # Load jinja2 template files.
    pkg = importlib.resources.files("mdsite")
    template_path = pkg / "template" / "template.html"
    css_path = pkg / "template" / css_file_name
    template = template_path.read_text()
    css = css_path.read_text()
    return template, css


def calc_link_to_root(path: Path) -> str:
    # Calculate relative path to the site root
    # When path is "in/foo/bar.md", returns "../"
    # When path is "in/index.md", return "./"
    if len(path.parts) == 2:
        return "./"
    else:
        return "../" * (len(path.parts) - 2)


def is_excluded(path: Path, config: dict) -> bool:
    if "excludes" not in config.keys():
        return False
    for exclude in config["excludes"]:
        print(path, exclude)
        if path.match(exclude):
            print(path, " is excluded")
            return True
    return False


def load_markdown_files(config: dict) -> list[MarkDownFile]:
    # Load .md files in input_dir, recursively.
    # Retuen a list of MarkDown instances.
    print("collecting target markdown files...")
    markdown_files = []
    input_paths = Path(config["input_dir"]).glob("**/*.md")
    for path in input_paths:
        print(path, " is detected")
        if is_excluded(path, config):
            continue
        output_dir = Path(config["output_dir"], *path.parts[1:-1])
        output_html_file_name = path.stem + ".html"
        output_path = Path(output_dir, output_html_file_name)
        stat = os.stat(path)
        if len(path.parts[1:-1]) > 0:
            link = "./".join(path.parts[1:-1]) + "/" + output_html_file_name
        else:
            link = output_html_file_name

        category = "/".join(path.parts[1:-1])
        link_to_root = calc_link_to_root(path)

        # Read All Documents
        with open(path) as f:
            contents = f.read()

        # Parse Title
        title = ""
        with open(path) as f:
            lines = f.readlines()
            for line in lines:
                if len(line) <= 1:
                    continue
                if line[0:2] == "# ":
                    title = line[2:]
                    break

        if platform.platform().find("macOS") != -1:
            created_at = stat.st_birthtime
        else:
            created_at = stat.st_ctime

        markdown_file = MarkDownFile(
            path=path,
            output_path=output_path,
            output_dir=output_dir,
            created_at=created_at,
            edited_at=stat.st_mtime,
            contents=contents,
            title=title,
            link=link,
            link_to_root=link_to_root,
            category=category,
        )
        markdown_files.append(markdown_file)
    print()
    return markdown_files


def make_output_dirs(markdown_files: list[MarkDownFile]):
    # Make output directories recursively
    for markdown_file in markdown_files:
        os.makedirs(markdown_file.output_dir, exist_ok=True)


def make_time_str(timestamp: str, config: dict) -> str:
    d = date.fromtimestamp(int(timestamp))
    return d.strftime(config["date_format"])


def convert_page(markdown_file: MarkDownFile, config: dict, template: str):
    # Convert a MarkDown instance into .html.
    markdown_html = markdown(
        markdown_file.contents, extensions=["fenced_code", "codehilite", "mdx_math"]
    )
    created_at = make_time_str(markdown_file.created_at, config)
    updated_at = make_time_str(markdown_file.edited_at, config)
    year = date.today().year
    template = Template(source=template)
    converted_html = template.render(
        contents=markdown_html,
        config=config,
        created_at=created_at,
        updated_at=updated_at,
        year=year,
        markdown=markdown_file,
    )
    with open(markdown_file.output_path, "w") as f:
        f.write(converted_html)


def convert(markdown_files: list[MarkDownFile], config: dict, templates: str):
    for markdown_file in markdown_files:
        convert_page(markdown_file, config, templates)


def write_css(css: str, config: dict):
    output_path = Path(config["output_dir"]) / css_file_name
    with open(output_path, "w") as f:
        f.write(css)


def write_static(config: dict):
    input_static_dir = Path(config["input_dir"], "static")
    output_dir = Path(config["output_dir"], "static")
    if os.path.exists(input_static_dir):
        shutil.copytree(input_static_dir, output_dir, dirs_exist_ok=True)


def main(config_file_name: str):
    config = parse_config(config_file_name)
    template, css = load_template()
    markdown_files = load_markdown_files(config)
    make_output_dirs(markdown_files)
    convert(markdown_files, config, (template))
    write_css(css, config)
    write_static(config)


def entrypoint():
    args = parse_command_line_args()
    if args.version == True:
        print_version()
    else:
        main(args.config)
