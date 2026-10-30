from pathlib import Path

from mdsite import mdsite

CONFIG = {
    "title": "test",
    "author": "test",
    "date_format": "%Y/%m/%d",
    "lang": "en",
}

CONTENTS = """# math

Inline $e^x$ and `$code$`.

$$
\\frac{1}{2}
$$

| Name | Value |
|:-----|------:|
| `a`  | 1     |
"""


def render(tmp_path: Path) -> str:
    template, _ = mdsite.load_template()
    markdown_file = mdsite.MarkDownFile(
        path=tmp_path / "index.md",
        output_path=tmp_path / "index.html",
        output_dir=tmp_path,
        created_at=0.0,
        edited_at=0.0,
        contents=CONTENTS,
        title="math",
        link="index.html",
        link_to_root="./",
        category="",
    )
    mdsite.convert_page(markdown_file, CONFIG, template)
    return (tmp_path / "index.html").read_text()


def test_template_loads_mathjax_4(tmp_path: Path) -> None:
    html = render(tmp_path)
    assert "https://cdn.jsdelivr.net/npm/mathjax@4/tex-chtml.js" in html
    # MathJax 2 の読み込みや設定が残っていない
    assert "mathjax@2" not in html
    assert "MathJax.Hub" not in html


def test_template_converts_mathjax_2_script_tags(tmp_path: Path) -> None:
    # python-markdown-math は MathJax 2 形式の script タグを出力するため、
    # テンプレート側で MathJax 4 の数式に変換する処理が必要になる
    html = render(tmp_path)
    assert '<script type="math/tex; mode=display">' in html
    assert 'script[type^="math/tex"]' in html


def test_inline_math_is_left_for_mathjax(tmp_path: Path) -> None:
    # インライン数式は MathJax が $...$ をページ上で処理する
    html = render(tmp_path)
    assert "Inline $e^x$ and <code>$code$</code>." in html
    assert "inlineMath: [ ['$','$']" in html


def test_template_uses_bundled_stylesheet(tmp_path: Path) -> None:
    # 外部の CSS フレームワークに依存せず、同梱の mdsite.css だけを読み込む
    html = render(tmp_path)
    assert '<link rel="stylesheet" href="./mdsite.css">' in html
    assert html.count('rel="stylesheet"') == 1
    assert "water.css" not in html


def test_stylesheet_keeps_pygments_section() -> None:
    # 独自スタイルを追加しても、Pygments の生成部分が末尾に残っている
    _, css = mdsite.load_template()
    own, generated = css.split("/* DO NOT EDIT UNDER THIS LINE */")
    assert "--background: #efefef;" in own
    assert ".codehilite" in generated


def test_table_is_rendered(tmp_path: Path) -> None:
    # Markdown の表が table 要素に変換される
    html = render(tmp_path)
    assert "<table>" in html
    assert '<th style="text-align: left;">Name</th>' in html
    assert '<td style="text-align: right;">1</td>' in html
    assert '<td style="text-align: left;"><code>a</code></td>' in html
