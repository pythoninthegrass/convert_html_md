# convert_html_md

## Summary
Extended version of the [Nimbus HTML to Markdown gist](https://gist.github.com/pythoninthegrass/61b7d738e85c32cec9c867a7a4e07306). 

Uses [pandodc](https://pandoc.org/) to convert HTML files with asset directories exported from Nimbus for use in other vendor-agnostic Markdown readers (cf. [UpNote](https://getupnote.com/)).

## Setup
* Install
    * [editorconfig](https://editorconfig.org/)
    * [asdf](https://asdf-vm.com/guide/getting-started.html#_2-download-asdf)
    * [poetry](https://python-poetry.org/docs/)
    * [justfile](https://just.systems/man/en/)

## Usage
```bash
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
