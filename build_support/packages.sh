#!/bin/bash

## =================================================================
## CS160 PACKAGE INSTALLATION
##
## This script will install all the packages that are needed to
## build and test your compiler: Python, clang, git, zip, and the
## ruff formatter and linter.
##
## It works on macOS, and on Linux with apt-get (Ubuntu, Debian),
## dnf (Fedora), pacman (Arch) or zypper (openSUSE), including under
## WSL 2. Then run python3 tools/doctor.py to check the versions.
## =================================================================

RUFF_VERSION=0.16.9
ROOT=$(cd "$(dirname "$0")/.." && pwd)

main() {
  set -o errexit

  if [ "$1" == "-y" ]
  then
    install
  else
    echo "PACKAGES WILL BE INSTALLED. THIS MAY BREAK YOUR EXISTING TOOLCHAIN."
    echo "YOU ACCEPT ALL RESPONSIBILITY BY PROCEEDING."
    read -p "Proceed? [y/N] : " yn

    case $yn in
      Y|y) install;;
      *) ;;
    esac
  fi

  echo "Script complete."
}

install() {
  set -x
  UNAME=$(uname | tr "[:lower:]" "[:upper:]" )

  case $UNAME in
    DARWIN) install_mac ;;

    LINUX) install_linux ;;

    *) install_other ;;
  esac

  install_ruff
}

install_other() {
  set +x
  echo "This script does not know how to install packages on $(uname -s):"
  echo "install Python, clang, git and zip yourself, then run this script again."
  set -x
}

install_mac() {
  # clang and git come with Apple's command-line tools.
  xcode-select -p > /dev/null 2>&1 || xcode-select --install
  # Install Homebrew.
  if test ! $(which brew); then
    echo "Installing Homebrew (https://brew.sh/)"
    bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
  fi
  # Update Homebrew.
  brew update
  # Install packages. The python3 that comes with the command-line tools is too old.
  brew ls --versions python || brew install python
}

install_linux() {
  # Use whichever package manager this distribution has.
  if command -v apt-get > /dev/null; then
    apt-get -y update
    apt-get -y install clang git python3 python3-venv zip
    # An older release's default clang cannot read the course's IR (its `ptr` needs LLVM 15):
    # install the newest clang the release offers, and make it the `clang` on PATH.
    major=$(clang --version 2> /dev/null | grep -o 'version [0-9]*' | head -1 | cut -d ' ' -f 2)
    if [ "${major:-0}" -lt 15 ]; then
      newest=$(apt-cache search --names-only '^clang-[0-9]+$' | cut -d ' ' -f 1 | sort -V | tail -1)
      if [ -n "$newest" ]; then
        apt-get -y install "$newest"
        ln -sf "/usr/bin/$newest" /usr/local/bin/clang
      fi
    fi
  elif command -v dnf > /dev/null; then
    dnf -y install clang git python3 zip
  elif command -v pacman > /dev/null; then
    pacman -Sy --noconfirm --needed clang git python zip
  elif command -v zypper > /dev/null; then
    zypper --non-interactive install clang git python3 zip
  else
    set +x
    echo "No apt-get, dnf, pacman or zypper here: install Python, clang, git"
    echo "and zip yourself, then run this script again."
    set -x
  fi
}

install_ruff() {
  # ruff goes into build_support/.venv, owned by you even when this script runs with sudo.
  if [ -n "$SUDO_USER" ]; then
    sudo -u "$SUDO_USER" python3 -m venv "$ROOT/build_support/.venv"
    sudo -u "$SUDO_USER" "$ROOT/build_support/.venv/bin/pip" install --quiet "ruff==$RUFF_VERSION"
  else
    python3 -m venv "$ROOT/build_support/.venv"
    "$ROOT/build_support/.venv/bin/pip" install --quiet "ruff==$RUFF_VERSION"
  fi
}

main "$@"
