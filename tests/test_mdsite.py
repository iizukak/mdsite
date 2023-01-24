from mdsite import mdsite
import os
import shutil


def test_main_with_no_output():
    shutil.rmtree("out", ignore_errors=True)
    shutil.copy("mdsite.yaml", "tests/mdsite.yaml")
    os.chdir("tests")
    mdsite.main("mdsite.yaml")


def test_main_2nd():
    mdsite.main("mdsite.yaml")
