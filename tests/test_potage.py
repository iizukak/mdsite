from potage import potage
import os
import shutil


def test_main_with_no_output():
    shutil.rmtree("out", ignore_errors=True)
    shutil.copy("potage.yaml", "tests/potage.yaml")
    os.chdir("tests")
    potage.main()


def test_main_2nd():
    potage.main()
