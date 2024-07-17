"""Utility functions that provide the absolute path to project directories.
"""

import os
from typing import Optional

import git
from git.exc import InvalidGitRepositoryError, NoSuchPathError


def find_project_root(marker='setup.cfg') -> str:
    """Find the absolute path to the project's root directory.

    Args:
        marker (str): The filename that identifies the root of the project.
        Defaults to 'setup.py'.

    Returns:
        str: The absolute path to the project's root directory.
    """
    current_dir = os.getcwd()
    while current_dir != os.path.dirname(current_dir):
        if marker in os.listdir(current_dir):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    raise FileNotFoundError(
        f"Could not find the project root. No {marker} found in any parent "
        "directories.")


def gitdir() -> str:
    """Find the absolute path to the GitHub repository root.
    """
    try:
        git_repo = git.Repo(os.getcwd(), search_parent_directories=True)
        git_root = git_repo.git.rev_parse('--show-toplevel')
        return git_root
    except (InvalidGitRepositoryError, NoSuchPathError):
        return find_project_root()


def datadir(path: str, mkdir: Optional[bool] = True) -> str:
    """The absolute path to the data directory.

    Data directory is for training and testing data. Here the path is created
    if it does not exist upon call if `mkdir` is True.

    Args:
        path: A string for directory name located at the data directory. mkdir:
        An optional boolean for whether to create the directory if it
            does not exist.
    """
    path = os.path.join(gitdir(), 'data/', path)
    if (not os.path.exists(path)) and mkdir:
        os.makedirs(path)
    return path


def plotsdir(path: str, mkdir: Optional[bool] = True) -> str:
    """The absolute path to the plot directory.

    Plot directory stores figure of experiment results. Here the path is
    created if it does not exist upon call if `mkdir` is True.

    Args:
        path: A string for directory name located at the plot directory. mkdir:
        An optional boolean for whether to create the directory if it
            does not exist.
    """
    path = os.path.join(gitdir(), 'plots/', path)
    if (not os.path.exists(path)) and mkdir:
        os.makedirs(path)
    return path
