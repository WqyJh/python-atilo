# python-atilo

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