# potage

[![example workflow](https://github.com/iizukak/potage/actions/workflows/test.yaml/badge.svg)](https://github.com/iizukak/potage/actions/workflows/test.yaml)

Minimal Static Site Generator.

[demo](https://iizukak.github.io/potage/),
[repository](https://github.com/iizukak/potage).

## What potage do

potage converts `.md` files into `.html` files in the same directory structure.

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

potage requires Python 3.7 or later and GNU Make.

```
$ git clone git@github.com:iizukak/potage.git
$ cd potage
$ make install
```

## Usage

### Command

Show help message.

```
$ potage help
```

Convert `.md` files into `.html` files.

```
$ potage
```

## Development

To develop or debug potage, You need additional Python libraries.

```
$ make devinstall
```

Unit testing.

```
$ make test
```

Run the demo site on the local server.

```
$ make demo
```

### Configuration

You should write some settings in `potage.yaml`.Please check this repository's root directory.

## Documentation Guide

- Converted `index.html` includes the automatically generated table of contents.
- Each MarkDown file's first `#` in will be the page title. We need at least one `#` in a doc.
- potage copies `static` directory to the output directory.

## FAQ

- Which CSS framework potage use?
    - [MVP.css](https://github.com/andybrewer/mvp/).

## License

[Apache License 2.0](https://spdx.org/licenses/Apache-2.0.html)