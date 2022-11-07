# convert_html_md

## Summary
Extended version of the [Nimbus HTML to Markdown gist](https://gist.github.com/pythoninthegrass/61b7d738e85c32cec9c867a7a4e07306). 

Uses [pandoc](https://pandoc.org/) to convert HTML files with asset directories exported from Nimbus for use in other vendor-agnostic Markdown readers (cf. [UpNote](https://getupnote.com/)).

## Setup
* Install
    * [editorconfig](https://editorconfig.org/)
    * [asdf](https://asdf-vm.com/guide/getting-started.html#_2-download-asdf)
    * [poetry](https://python-poetry.org/docs/)

## Usage
```bash
# activate a new virtual environment
python3 -m venv venv; . venv/bin/activate; pip install --upgrade pip
# install dependencies
python -m pip install -r requirements.txt

# run program from top-level directory
python convert.py
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
