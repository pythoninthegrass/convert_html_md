# See https://just.systems/man/en

# positional args
# * NOTE: unable to reuse recipe name (e.g., start/stop); prefix recipes with `@`
# set positional-arguments := true

# load .env
set dotenv-load

# set env var
# export APP      := `echo ${APP}`
# export SCRIPT   := "harden"
# export VERSION  := "latest"

# x86_64/arm64
arch := `uname -m`

# hostname
host := `uname -n`

# docker-compose / docker compose
# * https://docs.docker.com/compose/install/linux/#install-using-the-repository
# docker-compose := if `command -v docker-compose; echo $?` == "0" {
# 	"docker-compose"
# } else {
# 	"docker compose"
# }

# [halp]     list available commands
default:
    just --list

# [deps]     update dependencies
update-deps:
    #!/usr/bin/env bash
    # set -euxo pipefail
    find . -maxdepth 3 -name "pyproject.toml" -exec \
        echo "[{}]" \; -exec \
        echo "Clearring pypi cache..." \; -exec \
        poetry cache clear --all pypi --no-ansi \; -exec \
        poetry update --lock --no-ansi \;

# [deps]     export requirements.txt
export-reqs: update-deps
    #!/usr/bin/env bash
    # set -euxo pipefail
    find . -maxdepth 3 -name "pyproject.toml" -exec \
        echo "[{}]" \; -exec \
        echo "Exporting requirements.txt..." \; -exec \
        poetry export --no-ansi --without-hashes --output requirements.txt \;

# [git]      update git submodules
sub:
    git submodule update --init --recursive && git pull --recurse-submodules
