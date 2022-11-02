# potage

Minimal Static Site Generator.

The demo site is [here]().

## What potage do

potage converts .md files into .html files in the same directory structure.

For example, if you have these files,

```
in/index.md
in/foo/bar.md
in/static/image.jpeg
potage.yaml # Configulation files
```

by executing `potage` command, you will get these outputs.

```
out/index.html
out/foo/bar.html
out/static/image.jpeg
```

In the current directory, you should have `potage.yaml` configuration file.
Please check `Usage` section.

## Installation

potage requires Python 3.7 or later.

To install `potage`, execute the below commands.

```
$ git clone git@github.com:iizukak/potage.git
$ cd potage
$ pip3 install -e .
```

If you want to debug potage, Please execute

```
$ pip3 install -e ".[dev]"
```

## Usage

### Command

To show help message, please execute

```
$ potage help
```

To convert .md to .html, type `potage` without argument.

```
$ potage
```

### Configuration

You should write some settings in `potage.yaml`.
Here is the template.

```yaml
title: Taro Yamada's Home Page
author: Taro Yamada
input_dir: in
output_dir: out
date_format: YYYYMMDD
```

### Unit Test

```
$ pytest .
```

## Documentation Guide

- Converted `index.html` includes the automatically generated table of contents.
- Each MarkDown file's first `#` in will be the page title.
- potage copy `static` directory to the output directory.

## FAQ

- Why potage generates poorly styled sites?
  - For the minimalism, potage use user agent (browsers default) stylesheets with minimal modification.
  - I assume that user agent stylesheets will maintain by Browser developers. The lifespan is long enough.
- Can I change CSS template?
  - NO. If you want to change templates, Please fork potage and change `template/potage.css`.
- Can I change config file name?
  - NO

## License

[Apache License 2.0](https://spdx.org/licenses/Apache-2.0.html)