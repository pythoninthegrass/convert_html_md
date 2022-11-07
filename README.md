# convert_html_md

## Summary
Extended version of the [Nimbus HTML to Markdown gist](https://gist.github.com/pythoninthegrass/61b7d738e85c32cec9c867a7a4e07306). 

Uses [pandoc](https://pandoc.org/) to convert HTML files with asset directories exported from Nimbus for use in other vendor-agnostic Markdown readers (cf. [UpNote](https://getupnote.com/)).

**Table of Contents**
* [convert_html_md](#convert_html_md)
  * [Summary](#summary)
  * [Setup](#setup)
    * [Dependencies](#dependencies)
  * [Usage](#usage)
  * [TODO](#todo)
  * [Further Reading](#further-reading)

## Setup
* Install
    * [editorconfig](https://editorconfig.org/)
    * [asdf](https://asdf-vm.com/guide/getting-started.html#_2-download-asdf)
    * [poetry](https://python-poetry.org/docs/)

### Dependencies
`pip` comes with python by default and is sufficient to get up and running quickly. `asdf` is a wrapper for `pyenv` (among other runtimes) and takes care of python versions. `poetry` handles dependencies, virtual environments, and packaging.

* `pip`
    ```bash
    # activate a new virtual environment
    python3 -m venv .venv; . .venv/bin/activate; pip3 install --upgrade pip

    # install dependencies
    python3 -m pip install -r requirements.txt
    ```
* `asdf`
    ```bash
    # add python plugin
    asdf plugin-add python

    # install stable python
    asdf install python <latest>  # 3.10.8

    # uninstall version
    asdf uninstall python latest

    # refresh symlinks for installed python runtimes
    asdf reshim python

    # set working directory version (i.e., repo)
    asdf local python latest

    # set stable to system python
    asdf global python latest
    ```
* `poetry`
    ```bash
    # Install
    curl -sSL https://install.python-poetry.org | $(which python3) -

    # Uninstall
    export POETRY_UNINSTALL=1
    curl -sSL https://install.python-poetry.org | $(which python3) -

    # Change config
    poetry config virtualenvs.in-project true           # .venv in `pwd`

    # Install from requirements.txt
    poetry add `cat requirements.txt`

    # Update dependencies
    poetry update

    # Remove library
    poetry remove <lib>

    # Generate requirements.txt
    poetry export -f requirements.txt --output requirements.txt --without-hashes
    ```
* Poetry with `asdf`
    ```bash
    # Add poetry asdf plugin
    asdf plugin-add poetry https://github.com/asdf-community/asdf-poetry.git

    # Install latest version via asdf
    asdf install poetry latest

    # Set latest version as default
    asdf global poetry latest

    # Install via asdf w/version
    ASDF_POETRY_INSTALL_URL=https://install.python-poetry.org asdf install poetry 1.2.2
    asdf local poetry 1.2.2
    ```

## Usage
* Virtual environment
    ```bash
    # source virtual environment (venv) from dependencies setup above
    . .venv/bin/activate

    # run program from top-level directory
    python3 convert.py

    # exit
    deactivate
    ```
* Poetry
    ```bash
    # Run script and exit environment
    poetry run python convert.py

    # Activate virtual environment (venv)
    poetry shell

    # Run script
    python convert.py

    # Deactivate venv
    exit  # ctrl-d
    ```

## TODO
* ~~Document usage~~
* Parallelize with `joblib`
* Benchmark
  * 3.10.8
  * 3.11.0
  * Pre/post-parallelization
* [Open Issues](https://github.com/pythoninthegrass/convert_html_md/issues)

## Further Reading
[Convert Nimbus Notes HTML to Markdown for Joplin](https://gist.github.com/aolle/6e595650391deef79ffb1c9bb38fb6e9)

[Python decorator to measure execution time - DEV Community 👩‍💻👨‍💻](https://dev.to/kcdchennai/python-decorator-to-measure-execution-time-54hk)

[The Boilerplate for Logging in Python | by Ezz El Din Abdullah | Brainwave | Medium](https://medium.com/the-brainwave/the-boilerplate-for-logging-in-python-105952585f39)

[Run Code after Your Program Exits with Python’s AtExit | by Mike Huls | Sep, 2022 | Towards Data Science](https://towardsdatascience.com/run-code-after-your-program-exits-with-pythons-atexit-82a0069b486a)

[Replace multiple spaces with a single space in Python | bobbyhadz](https://bobbyhadz.com/blog/python-replace-multiple-spaces-with-single-space)

[Python's zipfile: Manipulate Your ZIP Files Efficiently – Real Python](https://realpython.com/python-zipfile/#building-a-zip-file-from-a-directory)
