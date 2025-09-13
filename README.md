# Quickperms
Quick Permission Library Inspired by LuckPerms
![Static Badge](https://img.shields.io/badge/python-3.13-blue?logo=python)


## Installation
Using `pip`
```bash
pip install quickperms
```
Using `uv`
```bash
uv add quickperms
```

## Configuration
Quickperms uses environment variables to get database info.
`VALKEY_HOST` == `localhost`or`valkey://valkey-container`or`https://example.com/valkey-db`
`VALKEY_PORT` == `6379`
`VALKEY_DB` == `0` or may be 0-15
`VALKEY_PASS` == unset or`password`


## Usage
#### Set environment variables and then import the library
Using `os`
```python
import os
os.environ['VALKEY_HOST'] = 'localhost'
os.environ['VALKEY_PORT'] = '6379'
os.environ['VALKKEY_DB'] = '0'
os.environ['VALKKEY_PASS'] =  ''
from quickperms import qset, qcheck
```
<br>
Using `dotenv`
```python
from dotenv import load_dotenv
load_dotenv()
from quickperms import qset, qcheck
```
.env file
```txt
VALKEY_HOST=localhost
VALKEY_PORT=6379
VALKEY_DB=0
```
<br>

## Quick Reference
`vset(uid: str, permission: str, glob: str)` - TODO

`vcheck(uid: str, permission: str, glob: str)` - TODO
