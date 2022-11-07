#!/usr/bin/env python3

# flake8: noqa

# fmt: off
# import atexit
import logging
import pandas as pd
import shutil
import subprocess
import time
from colorama import Fore
from functools import wraps
# from joblib import Parallel, delayed
from pathlib import Path
from pathvalidate import replace_symbol
from shlex import quote
from zipfile import ZipFile
# fmt: on

# logging prefixes
info = "INFO:"
error = "ERROR:"
warning = "WARNING:"

# Define a logger instance
logger = logging.getLogger(__name__)

# Define a stream handler for the console output
handler = logging.StreamHandler()  # Customize the formatter on the console
formatter = logging.Formatter("[ %(asctime)s %(name)s ] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# Add the formatter to the handler
handler.setFormatter(formatter)  # Add the stream handler to the logger that we will use
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

# exclude files
exclude_list = ["archive", "nimbus_export", "subset"]


def unzip_files():
    """Unzip files in the current directory"""

    # iterate through exclude list with pathlib rglob
    for _ in Path(".").rglob("*"):
        if any(x in _.name for x in exclude_list):
            logger.info(f"{Fore.GREEN}{info:<10}{Fore.RESET}Skipping {_.name}")
            continue
        if _.suffix == ".zip":
            logger.info(f"{Fore.GREEN}{info:<10}{Fore.RESET}Unzipping {_.name}")
            with ZipFile(_) as zip_file:
                zip_file.extractall(path=f"{_.parent}/{_.stem}")


def write_note(html_file, markdown_destination):
    """Convert html file to markdown and write to original directory"""

    global notes_written, notes_failed

    dest = Path(f"{markdown_destination}").resolve()

    logger.info(f"{Fore.GREEN}{info:<10}{Fore.RESET}Writing markdown to {dest}")

    # escape quotes with shlex
    html_file = quote(str(html_file))

    # convert html to markdown
    cmd = f"pandoc {html_file} --from html --to markdown_strict-raw_html"

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


# @atexit.register
def cleanup_zip_files():
    """Remove zip files in the current directory"""

    # iterate through exclude list with pathlib rglob
    for _ in Path(".").rglob("*"):
        if any(x in _.name for x in exclude_list):
            logger.info(f"{Fore.GREEN}{info:<10}{Fore.RESET}Skipping {_.name}")
            continue
        if _.suffix == ".zip":
            logger.info(f"{Fore.GREEN}{info:<10}{Fore.RESET}Removing {_.name}")
            _.unlink()


# @atexit.register
def move_empties():
    """Move empty markdown files"""

    # create archive directory
    archive_dir = Path("./archive")
    archive_dir.mkdir(exist_ok=True)

    empties = [i for i in Path(".").rglob("*.md")]

    for _ in empties:
        if _.stat().st_size == 1:
            logger.info(f"{Fore.GREEN}{info:<10}{Fore.RESET}Archiving empty directory {_.parent.name}")

            # move makdown directory to archive directory
            try:
                shutil.move(f"{_.parent}", f"./archive/")
            except shutil.Error:
                logger.error(f"{Fore.RED}{error:<10}{Fore.RESET}Failed to move {_.parent.name} to archive directory")
                continue

    # zip archive directory
    if Path(f"{archive_dir}.zip").exists():
        logger.info(f"{Fore.GREEN}{info:<10}{Fore.RESET}Archive directory already exists, skipping")
    else:
        with ZipFile(f"{archive_dir}.zip", mode="w") as zip_file:
            for file_path in archive_dir.rglob("*"):
                zip_file.write(file_path, arcname=file_path.relative_to(archive_dir))

    # remove archive directory
    try:
        shutil.rmtree("./archive")
    except shutil.Error:
        logger.error(f"{Fore.RED}{error:<10}{Fore.RESET}Failed to remove archive directory")


@timeit
def main():
    # unzip files
    unzip_files()

    # TODO: add joblib parallelization after getting results of html files
    # get html files
    html_files = [i for i in Path(".").rglob("*.html")]

    # convert html files to markdown
    for _ in html_files:
        html_file = _.absolute()

        # directory name
        dirname = html_file.parent.name

        # sanitize filepath
        sanitized = replace_symbol(dirname, exclude_symbols=[" ", "_", "-"])

        # fix double whitespace
        sanitized = " ".join(sanitized.split())

        # rename directory to sanitized filepath with pathlib
        filepath = Path(f"{html_file.parent.parent}/{sanitized}")
        try:
            html_file.parent.rename(filepath)
        except OSError:
            logger.error(f"{Fore.RED}{error:<10}{Fore.RESET}Failed to rename {html_file.parent.name} to {sanitized}")
            continue

        # filename
        filename = html_file.stem + ".md"

        # resolve new html file path
        html_file = Path(f"{filepath}/{html_file.name}").resolve()

        # create markdown file name
        md_destination = Path(filepath / filename).absolute()

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

    # QA-only; use `@atexit.register`
    cleanup_zip_files()
    move_empties()


if __name__ == "__main__":
    main()
