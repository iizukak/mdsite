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
"""


def render(tmp_path: Path) -> str:
    template, _ = mdsite.load_template()
    markdown_file = mdsite.MarkDownFile(
        path=tmp_path / "index.md",
        output_path=tmp_path / "index.html",
        output_dir=tmp_path,
        created_at=0,
        edited_at=0,
        contents=CONTENTS,
        title="math",
        link="index.html",
        link_to_root="./",
        category="",
    )
    mdsite.convert_page(markdown_file, CONFIG, template)
    return (tmp_path / "index.html").read_text()


def test_template_loads_mathjax_4(tmp_path):
    html = render(tmp_path)
    assert "https://cdn.jsdelivr.net/npm/mathjax@4/tex-chtml.js" in html
    # MathJax 2 の読み込みや設定が残っていない
    assert "mathjax@2" not in html
    assert "MathJax.Hub" not in html


def test_template_converts_mathjax_2_script_tags(tmp_path):
    # python-markdown-math は MathJax 2 形式の script タグを出力するため、
    # テンプレート側で MathJax 4 の数式に変換する処理が必要になる
    html = render(tmp_path)
    assert '<script type="math/tex; mode=display">' in html
    assert 'script[type^="math/tex"]' in html


def test_inline_math_is_left_for_mathjax(tmp_path):
    # インライン数式は MathJax が $...$ をページ上で処理する
    html = render(tmp_path)
    assert "Inline $e^x$ and <code>$code$</code>." in html
    assert "inlineMath: [ ['$','$']" in html
