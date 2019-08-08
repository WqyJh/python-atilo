# python-atilo

[atilo](https://github.com/YadominJinta/atilo) written in python.

## Installation

TODO

## Usage

### Show available releases
```bash
$ python atilo.py list
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
$ python atilo.py list --installed
alpine3.9
debianbuster
```

### Install a release

```bash
# Install the latest debian release
python atilo.py install debian

# Install specified debian release
python atilo.py install debian jessie
```

### Run a release

```bash
# Start the debian jessie release
startdebianjessie
```

### Remove a release

```bash
python atilo.py debianbuster
```

### Clean temp files

```bash
python atilo.py clean
```