# mdsite

[![example workflow](https://github.com/iizukak/mdsite/actions/workflows/test.yaml/badge.svg)](https://github.com/iizukak/mdsite/actions/workflows/test.yaml)

Minimal Static Site Generator.

[demo](https://iizukak.github.io/mdsite/),
[repository](https://github.com/iizukak/mdsite).

## What mdsite do

mdsite converts `.md` files into `.html` files in the same directory structure.

For example, if you have these files,

```
in/index.md
in/foo/bar.md
in/static/image.jpeg
mdsite.yaml # Configulation files
```

by executing `mdsite` command, you will get these outputs.

```
out/index.html
out/foo/bar.html
out/static/image.jpeg
```

In the current directory, you should have `mdsite.yaml` configuration file.
Please check the [example config file](https://github.com/iizukak/mdsite/blob/main/mdsite.yaml).

## Installation

mdsite requires Python 3.8 or later and GNU Make.

```
$ git clone git@github.com:iizukak/mdsite.git
$ cd mdsite
$ make install
```

## Usage

### Command

Show help message.

```
$ mdsite help
```

Convert `.md` files into `.html` files.

```
$ mdsite
```

## Development

To develop or debug mdsite, You need additional Python libraries.

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

## Documentation Guide

- Converted `index.html` includes the automatically generated table of contents.
- Each MarkDown file's first `#` in will be the page title. We need at least one `#` in a doc.
- mdsite copies `static` directory to the output directory.

## FAQ

- Which CSS framework mdsite use?
    - [MVP.css](https://github.com/andybrewer/mvp/).

## License

[Apache License 2.0](https://spdx.org/licenses/Apache-2.0.html)
