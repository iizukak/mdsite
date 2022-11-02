# potage

Minimal Static Site Generator.

## What potage do

potage convert .md files into .html files in the same directory structure.

For example, if you have these files,

```
in/index.md
in/foo/bar.md
in/static/image.jpeg
potage.yaml
```

by executing `potage` command, you will get these outputs.

```
out/index.html
out/foo/bar.html
out/static/image.jpeg
```

`out/index.html` automatically includes a table of contents.

In the current directory, you should have `potage.yaml` configuration file.
Please check `Usage` section.

## Demo

The demo site is [here]().

## Installation

potage requires Python3.7 or later.

To install `potage`, execute the below commands.

```
$ git clone git@github.com:iizukak/potage.git
$ cd potage
$ pip3 install -e .
```

## Usage

### Command

To show help message, please execute

```
$ potage help
```

Usually, typing `potage` without argument is enough.

```
$ potage
```

### Configuration

You should write some settings in `potage.yaml`. The template is here.

```yaml
title: The Home Page
author: Taro Yamada
input_dir: in
output_dir: out
header_hooter_exclude_pages: # list that will not include header and footer
    - page1.md
```

## Unit Test

```
$ pytest .
```