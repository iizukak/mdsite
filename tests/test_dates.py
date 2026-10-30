import os
import subprocess
from pathlib import Path

import pytest

from mdsite import mdsite

# テストで使うコミット日時
# 実行環境のタイムゾーンによって日付が変わらないよう、UTC の正午にする
FIRST_COMMIT = "2020-01-01T12:00:00+0000"
FIRST_COMMIT_TS = 1577880000.0
SECOND_COMMIT = "2021-06-15T12:00:00+0000"
SECOND_COMMIT_TS = 1623758400.0
# ファイルシステムの最終更新日時として設定する値
MTIME_TS = 1704153600.0  # 2024-01-02T00:00:00Z


@pytest.fixture(autouse=True)
def isolate_git(tmp_path, monkeypatch):
    # ユーザーの git 設定（署名やフック）の影響を受けないようにする
    monkeypatch.setenv("GIT_CONFIG_GLOBAL", os.devnull)
    monkeypatch.setenv("GIT_CONFIG_NOSYSTEM", "1")
    # tmp_path より上位のディレクトリを Git リポジトリとして探索しない
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path.parent))


def git(repo: Path, *args: str, date: str | None = None):
    env = os.environ.copy()
    if date is not None:
        env["GIT_AUTHOR_DATE"] = date
        env["GIT_COMMITTER_DATE"] = date
    subprocess.run(
        ["git", "-c", "user.name=test", "-c", "user.email=test@example.com", *args],
        cwd=repo,
        env=env,
        check=True,
        capture_output=True,
    )


def commit(repo: Path, date: str, message: str = "commit"):
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message, date=date)


def set_mtime(path: Path):
    os.utime(path, (MTIME_TS, MTIME_TS), follow_symlinks=False)


def created_at(path: Path) -> float:
    return mdsite.get_created_at(path, os.stat(path))


def updated_at(path: Path) -> float:
    return mdsite.get_updated_at(path, os.stat(path))


def fallback_created_at(path: Path) -> float:
    # 作成日時が取得できる環境ではそれを、できない環境では最終更新日時を期待する
    stat = os.stat(path)
    return getattr(stat, "st_birthtime", stat.st_mtime)


@pytest.fixture
def repo(tmp_path) -> Path:
    # 1 回目のコミットで追加し、2 回目のコミットで更新したファイルを持つリポジトリ
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q")
    (repo / "page.md").write_text("# page\n")
    commit(repo, FIRST_COMMIT)
    (repo / "page.md").write_text("# page\n\nupdated\n")
    commit(repo, SECOND_COMMIT)
    set_mtime(repo / "page.md")
    return repo


def test_run_git_returns_stdout(repo):
    assert mdsite.run_git(["rev-parse", "--is-inside-work-tree"], repo / "page.md") == (
        "true\n"
    )


def test_run_git_outside_repository(tmp_path):
    path = tmp_path / "page.md"
    path.write_text("# page\n")
    assert mdsite.run_git(["status"], path) is None


def test_run_git_without_git_command(repo, monkeypatch):
    monkeypatch.setenv("PATH", "")
    assert mdsite.run_git(["status"], repo / "page.md") is None


def test_committed_file(repo):
    path = repo / "page.md"
    assert created_at(path) == FIRST_COMMIT_TS
    assert updated_at(path) == SECOND_COMMIT_TS


def test_committed_file_ignores_ctime_and_mtime(repo):
    # checkout や clone で属性が変わっても、コミット日時が使われる
    path = repo / "page.md"
    os.chmod(path, 0o600)
    set_mtime(path)
    assert created_at(path) == FIRST_COMMIT_TS
    assert updated_at(path) == SECOND_COMMIT_TS


def test_modified_file_uses_mtime_for_updated_at(repo):
    path = repo / "page.md"
    path.write_text("# page\n\nwork in progress\n")
    set_mtime(path)
    assert created_at(path) == FIRST_COMMIT_TS
    assert updated_at(path) == MTIME_TS


def test_untracked_file(repo):
    path = repo / "new.md"
    path.write_text("# new\n")
    set_mtime(path)
    assert created_at(path) == fallback_created_at(path)
    assert updated_at(path) == MTIME_TS


def test_ignored_file(repo):
    (repo / ".gitignore").write_text("ignored.md\n")
    commit(repo, SECOND_COMMIT)
    path = repo / "ignored.md"
    path.write_text("# ignored\n")
    set_mtime(path)
    assert created_at(path) == fallback_created_at(path)
    assert updated_at(path) == MTIME_TS


def test_file_outside_repository(tmp_path):
    path = tmp_path / "page.md"
    path.write_text("# page\n")
    set_mtime(path)
    assert created_at(path) == fallback_created_at(path)
    assert updated_at(path) == MTIME_TS


def test_renamed_file_follows_history(repo):
    git(repo, "mv", "page.md", "renamed.md")
    commit(repo, "2022-03-03T00:00:00+0000")
    assert created_at(repo / "renamed.md") == FIRST_COMMIT_TS


def test_symlink_uses_target_history(repo):
    # demo/index.md -> ../README.md のように、リンク先の履歴を参照する
    (repo / "demo").mkdir()
    link = repo / "demo" / "index.md"
    link.symlink_to(Path("..", "page.md"))
    commit(repo, "2023-04-04T00:00:00+0000")
    assert created_at(link) == FIRST_COMMIT_TS
    assert updated_at(link) == SECOND_COMMIT_TS


def test_main_writes_commit_dates(repo, monkeypatch):
    # サイト生成の結果、フッターにコミット日時が出力される
    (repo / "in").mkdir()
    git(repo, "mv", "page.md", "in/index.md")
    commit(repo, SECOND_COMMIT)
    (repo / "mdsite.yaml").write_text(
        "title: test\n"
        "author: test\n"
        "input_dir: in\n"
        "output_dir: out\n"
        'date_format: "%Y/%m/%d"\n'
        "lang: en\n"
    )
    monkeypatch.chdir(repo)
    mdsite.main("mdsite.yaml")
    html = (repo / "out" / "index.html").read_text()
    assert "created at: 2020/01/01, updated at: 2021/06/15" in html
