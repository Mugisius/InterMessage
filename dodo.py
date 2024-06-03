'''
Default: create wheel
'''
import glob
import os
import tomllib
LINGOS = ("ru_RU",)
DOMINE = "IM"
DOIT_CONFIG = {'default_tasks': ['mo']}
with open("pyproject.toml", "rb") as pf:
    PYPROJECT = tomllib.load(pf)
    UTILITY = tuple(PYPROJECT["project"]["scripts"].keys())[0]
    PROJECT = PYPROJECT["project"]["name"]


def task_pot():
    '''Scan .py files and create a pot'''
    return {
        'actions': [f"pybabel extract -o {DOMINE}.pot {PROJECT}"],
        'file_dep': glob.glob(f"{PROJECT}/*.py", recursive=True),
        'targets': [f"{DOMINE}.pot"],
    }


def task_po():
    '''Update/create .po for all languages'''
    for lang in LINGOS:
        tgt = f"po/{lang}/LC_MESSAGES/{DOMINE}.po"
        yield {
            'name': f"{lang}.po",
            'actions': [
                    (os.makedirs, [f"po/{lang}/LC_MESSAGES"], {"exist_ok": True}),
                    f"pybabel update -l{lang} --ignore-pot-creation-date -D{DOMINE} -i{DOMINE}.pot -d po",
            ],
            'file_dep': [f"{DOMINE}.pot"],
            'targets': [f"{tgt}"],
        }


def task_mo():
    '''Compile .mo for all languages'''
    for lang in LINGOS:
        yield {
            'name': f"{lang}.mo",
            'actions': [
                (os.makedirs, [f"{PROJECT}/{lang}/LC_MESSAGES"], {"exist_ok": True}),
                f"pybabel compile -D{DOMINE} -l{lang} -i po/{lang}/LC_MESSAGES/{DOMINE}.po -d {PROJECT}",
            ],
            'file_dep': [f"po/{lang}/LC_MESSAGES/{DOMINE}.po"],
            'targets': [f"po/{lang}/LC_MESSAGES/{DOMINE}.mo"],
        }


def task_app():
    """Run application."""
    import InterMessage.InterMessage
    return {
        'actions': [InterMessage.InterMessage.main],
        'task_dep': ['mo'],
    }


def task_style():
    """Check style against flake8."""
    return {
        'actions': ['flake8 InterMessage']
    }


def task_docstyle():
    """Check docstrings against pydocstyle."""
    return {
        'actions': ['pydocstyle InterMessage']
    }


def task_test():
    """Make HTML documentationi."""
    return {
        'actions': [
            'python tests/TestValidate.py -v',
            'python tests/TestAttachment.py -v',
        ],
    }


def task_check():
    """Perform all checks."""
    return {
        'actions': None,
        'task_dep': ['style', 'docstyle']
    }


def task_html():
    """Make HTML documentationi."""
    return {
        'actions': ['sphinx-build -M html docs build'],
    }


def task_erase():
    return {
        'actions': ['git clean -xdf'],
    }


def task_wheel():
    return {
        'actions': ['pyproject-build -w'],
        'task_dep': ['mo'],
    }
