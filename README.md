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

mdsite requires Python 3.10 or later, [uv](https://docs.astral.sh/uv/) and GNU Make.

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

### Table

Tables are supported.

```
| Name   | Description                   |
|--------|-------------------------------|
| mdsite | Minimal Static Site Generator |
```

is converted to

| Name   | Description                   |
|--------|-------------------------------|
| mdsite | Minimal Static Site Generator |

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

## Japanese sample

The following is a sample in Japanese, written like a thread on 2channel.

### 【静的サイト】mdsite 総合スレ Part1

#### 1 ：名無しさん：2026/10/30(木) 12:00:00

Markdown から静的サイトを作るツール mdsite について語るスレです。

- 公式: [https://github.com/iizukak/mdsite](https://github.com/iizukak/mdsite)
- デモ: [https://iizukak.github.io/mdsite/](https://iizukak.github.io/mdsite/)

荒らしは放置でお願いします。

#### 2 ：名無しさん：2026/10/30(木) 12:00:12

2げっと

#### 3 ：名無しさん：2026/10/30(木) 12:03:45

> 2げっと

ずさーっ

#### 4 ：名無しさん：2026/10/30(木) 12:10:21

インストール方法を教えてください。

#### 5 ：名無しさん：2026/10/30(木) 12:15:08

> インストール方法を教えてください。

uv と GNU Make が入っていれば、これだけでいけます。

```
$ git clone git@github.com:iizukak/mdsite.git
$ cd mdsite
$ make install
```

あとは `mdsite.yaml` を置いたディレクトリで `mdsite` を実行するだけです。

#### 6 ：名無しさん：2026/10/30(木) 12:20:33

対応している書き方をまとめてみた。

| 書き方 | 対応 | 備考 |
|:-------|:----:|:-----|
| 見出し | ○ | `#` から `######` まで |
| 表 | ○ | 列ごとの左寄せ・中央・右寄せも可 |
| コード | ○ | 言語を書くと色が付く |
| 数式 | ○ | MathJax で表示 |

#### 7 ：名無しさん：2026/10/30(木) 12:25:47

コードに色が付くのはいいね。

```python
def greet(name: str) -> str:
    return f"こんにちは、{name}さん"


print(greet("名無し"))
```

#### 8 ：名無しさん：2026/10/30(木) 12:31:02

数式も書けるのか。$e^{i\pi} + 1 = 0$ みたいな行内の式も、

$$
\sum_{k=1}^{n} k = \frac{n(n+1)}{2}
$$

みたいな独立した式もいける。

#### 9 ：名無しさん：2026/10/30(木) 12:40:59

今どき静的サイトジェネレータとか誰が使うんだよ

#### 10 ：名無しさん：2026/10/30(木) 12:41:30

```
　　 ∧＿∧
　　（　´∀｀）＜　オマエモナー
```

#### 11 ：名無しさん：2026/10/30(木) 12:50:14

手順をまとめると、

1. `mdsite.yaml` を書く
2. `in/` に Markdown を置く
3. `mdsite` を実行する
4. `out/` に HTML ができる

---

このスレッドは過去ログ倉庫に格納されています。

## FAQ

- Which CSS framework mdsite use?
    - None. mdsite has its own stylesheet (`mdsite.css`) inspired by the design of 2channel in the Heisei era.
- Which font mdsite use?
    - [DotGothic16](https://github.com/fontworks-fonts/DotGothic16) by Fontworks Inc. is bundled to reproduce the look of bitmap fonts on old Windows browsers.
      It is copied to the output directory with its license (`DotGothic16-OFL.txt`).

## License

[Apache License 2.0](https://spdx.org/licenses/Apache-2.0.html)

The bundled font DotGothic16 is licensed under the [SIL Open Font License 1.1](https://openfontlicense.org/).