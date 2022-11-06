#!/usr/bin/env python3

"""
SOURCES:
https://gist.github.com/aolle/6e595650391deef79ffb1c9bb38fb6e9
https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk
https://medium.com/the-brainwave/the-boilerplate-for-logging-in-python-105952585f39
https://towardsdatascience.com/run-code-after-your-program-exits-with-pythons-atexit-82a0069b486a
https://bobbyhadz.com/blog/python-replace-multiple-spaces-with-single-space
"""

import atexit
import logging
import pandas as pd
import subprocess
import time
from colorama import Fore
from functools import wraps
# from icecream import ic
from pathlib import Path
from pathvalidate import replace_symbol
from zipfile import ZipFile

# logging prefixes
info = "INFO:"
error = "ERROR:"
warning = "WARNING:"

# Define a logger instance
logger = logging.getLogger(__name__)

# Define a stream handler for the console output
handler = logging.StreamHandler()# Customize the formatter on the console
formatter = logging.Formatter(
    "[ %(asctime)s %(name)s ] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
    )

# Add the formatter to the handler
handler.setFormatter(formatter)# Add the stream handler to the logger that we will use
logger.addHandler(handler)

# Set the level of logging to be INFO instead of the default WARNING
logger.setLevel(logging.INFO)


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        logger.info(f"{Fore.GREEN}{info:<10}{Fore.RESET}Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds")
        return result

    return timeit_wrapper


notes_written = 0
notes_failed = 0

win_dict = {}
fail_dict = {}


def unzip_files():
    """Unzip files in the current directory"""

    for _ in Path(".").rglob("*.zip"):
        if _.stem in [_.name for _ in Path(".").iterdir()]:
            logger.info(f"{Fore.GREEN}{info:<10}{Fore.RESET}Skipping {_}, already extracted")
            continue
        logger.info(f"{Fore.GREEN}{info:<10}{Fore.RESET}Unzipping {_}")
        try:
            with ZipFile(_) as zip_file:
                zip_file.extractall(path=_.stem)
        except ZipFile.BadZipFile:
            logger.error(f"{Fore.RED}{error:<10}{Fore.RESET}Skipping {_}, not a zip file")


@atexit.register
def cleanup_zip_files():
    """Remove zip files in the current directory"""

    for _ in Path(".").rglob("*.zip"):
        logger.info(f"{Fore.GREEN}{info:<10}{Fore.RESET}Removing {_}")
        _.unlink()


def write_note(html_file, markdown_destination):
    """Convert html file to markdown and write to original directory"""

    global notes_written, notes_failed

    dest = Path(f"{markdown_destination}").resolve()

    logger.info(f"{Fore.GREEN}{info:<10}{Fore.RESET}Writing markdown to {dest}")

    cmd = f"pandoc '{html_file}' --from html --to markdown_strict-raw_html"

    try:
        pandoc_run = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
        if markdown_destination.exists():
            logger.info(f"{Fore.GREEN}{info:<10}{Fore.RESET}Markdown file {dest} already exists, skipping")
            return
        else:
            with open(markdown_destination, "w", encoding="utf-8") as md_fp:
                md_content = pandoc_run.decode()
                md_fp.write(md_content)
            notes_written += 1
            win_dict[notes_written] = html_file
    except (FileNotFoundError, subprocess.CalledProcessError):
        logger.error(f"{Fore.RED}{error:<10}{Fore.RESET}Failed to convert {html_file}")
        notes_failed += 1
        fail_dict[notes_failed] = html_file


# TODO: error handling for tld retaining nested dirs (e.g., 'All Notes' vs. 'Books')
@timeit
def main():
    # unzip files
    unzip_files()

    # TODO: add joblib parallelization after getting results of html files
    # get html files
    html_files = [_.resolve() for _ in Path(".").rglob("*.html")]

    # convert html files to markdown
    for _ in html_files:
        html_file = _.resolve()

        # directory name
        dirname = html_file.parent.name

        # sanitize filepath
        sanitized = replace_symbol(dirname, exclude_symbols=[" ", "_", "-"])

        # fix double whitespace
        sanitized = " ".join(sanitized.split())

        # rename directory to sanitized filepath with pathlib
        filepath = html_file.parent.rename(sanitized)

        # filename
        filename = html_file.stem + ".md"

        # resolve new html file path
        html_file = Path(f"{filepath}/{html_file.name}").resolve()

        # create markdown file name
        md_destination = Path(f"{filepath}/{filename}")

        if md_destination.exists():
            dest = Path(f"{md_destination}").resolve()
            logger.info(f"{Fore.GREEN}{info:<10}{Fore.RESET}Markdown file {dest} already exists, skipping")
            continue
        write_note(html_file, md_destination)

    logger.info(f"{Fore.GREEN}{info:<10}{Fore.RESET}Converted {notes_written} notes, failed to convert {notes_failed} notes")

    # create dataframe
    wins = pd.DataFrame.from_dict(win_dict, orient="index", columns=["note"])
    fails = pd.DataFrame.from_dict(fail_dict, orient="index", columns=["note"])

    # write the dataframe to a csv file
    df = pd.DataFrame(wins)
    df.to_csv("win_list.csv", index=False)

    df = pd.DataFrame(fails)
    df.to_csv("fail_list.csv", index=False)


if __name__ == "__main__":
    main()
