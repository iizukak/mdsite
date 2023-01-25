# mdsite

[![example workflow](https://github.com/iizukak/mdsite/actions/workflows/test.yaml/badge.svg)](https://github.com/iizukak/mdsite/actions/workflows/test.yaml)

mdsite is a command line tool that generates a static site from Markdown files.

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
out/mdsite.css
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
$ make demoserver
```

## Documentation Guide

- Converted `index.html` includes the automatically generated table of contents.
- Each MarkDown file's first `#` in will be the page title. We need at least one `#` in a doc.
- mdsite copies `static` directory to the output directory.

### Syntax highlighting

Syntax highlighting is supported. Use triple `` ` `` to write the code.

````
```python
def hello():
    print("Hello, mdsite")
```
````

is converted to

```python
def hello():
    print("Hello, mdsite")
```

### MathJax Support

Math equations are supported by [python-markdown-math](https://github.com/mitya57/python-markdown-math).

#### Inline equation

Using single `$` generate inline equation.
For example, `$e^x$` is converted to $e^x$ .


#### Standalone equation

Using double `$` generates a standalone equation.
For example,

```tex
$$
\frac{1}{\Bigl(\sqrt{\phi \sqrt{5}}-\phi\Bigr) e^{\frac25 \pi}} =
1+\frac{e^{-2\pi}} {1+\frac{e^{-4\pi}} {1+\frac{e^{-6\pi}}
{1+\frac{e^{-8\pi}} {1+\ldots} } } }
$$
```

is converted to

$$
\frac{1}{\Bigl(\sqrt{\phi \sqrt{5}}-\phi\Bigr) e^{\frac25 \pi}} =
1+\frac{e^{-2\pi}} {1+\frac{e^{-4\pi}} {1+\frac{e^{-6\pi}}
{1+\frac{e^{-8\pi}} {1+\ldots} } } }
$$

## FAQ

- Which CSS framework mdsite use?
    - [MVP.css](https://github.com/andybrewer/mvp/).

## License

[Apache License 2.0](https://spdx.org/licenses/Apache-2.0.html)