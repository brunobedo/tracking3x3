from pathlib import Path


def get_project_dir():
    return str(Path.cwd().parent).replace('\\','/')