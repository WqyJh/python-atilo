# python-atilo

[![Build Status](https://travis-ci.org/WqyJh/python-atilo.svg?branch=master)](https://travis-ci.org/WqyJh/python-atilo)
[![license](https://img.shields.io/badge/LICENCE-GPLv3-brightgreen.svg)](https://raw.githubusercontent.com/WqyJh/python-atilo/master/LICENSE)


Install linux on termux.

[atilo](https://github.com/YadominJinta/atilo) written in python.


## Installation

```bash
pip install atilo
```

## Usage

### Show available releases
```bash
$ atilo list
name                version                       
alpine      2.7 3.9                       
centos      7                             
debian      jessie stretch buster         
fedora      30                            
kali                                      
parrot                                    
ubuntu      trusty xenial bionic 
```

### Show installed releases

```bash
$ atilo list --installed
alpine3.9
debianbuster
```

### Install a release

```bash
# Install the latest debian release
atilo install debian

# Install specified debian release
atilo install debian jessie
```

### Run a release

```bash
# Start the debian jessie release
startdebianjessie
```

### Remove a release

```bash
atilo debianbuster
```

### Clean temp files

```bash
atilo clean
```


## Contribute

### Prerequisite

- Python >= 3
- pipenv


### Requirements

```bash
pipenv install --dev
```

### Run

```bash
python run.py
```

### Generate Changelog (For Maintainers Only)

Install python tool `auto-changelog` to generate changelog.

```bash
sudo pip3 install git+https://github.com/Michael-F-Bryan/auto-changelog
```

Generate and write changelog to `CHANGELOG.md`.

```bash
auto-changelog
```

### Bump Version (For Maintainers Only)

```bash
sudo pip3 install commitizen
```

Using `commitizen` tool to generate semantic version number.

```bash
$ cz bump
[NO_VERSION_SPECIFIED]
Check if current version is specified in config file, like:
version = 0.4.3
```

Edit the `atilo/__init__.py`, set the `__version__` value to `'0.4.3'` (semantic version generated above).