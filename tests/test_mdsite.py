import shutil
from pathlib import Path

import pytest

from mdsite import mdsite

TESTS_DIR = Path(__file__).parent
ROOT_DIR = TESTS_DIR.parent
OUTPUT_DIR = TESTS_DIR / "out"


@pytest.fixture
def in_tests_dir(monkeypatch: pytest.MonkeyPatch) -> None:
    # tests/ でサイトを生成する。テスト終了後は元の作業ディレクトリに戻る
    shutil.copy(ROOT_DIR / "mdsite.yaml", TESTS_DIR / "mdsite.yaml")
    monkeypatch.chdir(TESTS_DIR)


def assert_outputs() -> None:
    assert (OUTPUT_DIR / "index.html").is_file()
    assert (OUTPUT_DIR / "dir" / "subdir.html").is_file()
    assert (OUTPUT_DIR / "mdsite.css").is_file()
    # 同梱フォントとそのライセンスが CSS と同じ場所に出力される
    assert (OUTPUT_DIR / "DotGothic16-Regular.woff2").is_file()
    assert (OUTPUT_DIR / "DotGothic16-OFL.txt").is_file()
    assert (OUTPUT_DIR / "static" / "sample.jpg").is_file()


def test_main_with_no_output(in_tests_dir: None) -> None:
    shutil.rmtree(OUTPUT_DIR, ignore_errors=True)
    mdsite.main("mdsite.yaml")
    assert_outputs()


def test_main_2nd(in_tests_dir: None) -> None:
    # 出力済みのディレクトリに対して、再度生成できる
    mdsite.main("mdsite.yaml")
    mdsite.main("mdsite.yaml")
    assert_outputs()
