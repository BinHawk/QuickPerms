# Quickperms
Quick Permission Library Inspired by LuckPerms

![Static Badge](https://img.shields.io/badge/python-3.13-blue?logo=python)

Quickperms allows you to assign and quickly check a User ID string to a permission.
Permissions have full globbing support and levels are seperated by a `.`

<br>

For Example:

`foo.bar` - will only match the `foo.bar` permission

`foo.*` - will match `foo.bar` `foo.baz` `foo.qux` ...

`foo.**` - will match `foo.bar` `foo.bar.baz` `foo.bar.baz.qux` ...

None of these permissions match just `foo`

<br>

Lets assume we have the user `john` and we want to give him permission to start a game server. We could...

```python
vset('john', 'gameserver.start')
# then
vcheck('john', 'gameserver.start') == True
```

But this command doesnt give `john` access to `gameserver.start.date` permission. Lets assign him access to everything under `gameserver.start`

```python
vset('john`, 'gameserver.start.*')
# Then
vcheck('john', 'gameserver.start.date') == True
vcheck('john', 'gameserver.start.foo') == True
vcheck('john', 'gameserver.start.bar') == True
```

In the future `john` might need to stop and start the server. Lets assign him every single permission under gameserver

```python
vset('john`, 'gameserver.**')
# Then
vcheck('john', 'gameserver.stop') == True
vcheck('john', 'gameserver.stop.foobar') == True
vcheck('john', 'gameserver.restart') == True
vcheck('john', 'gameserver.start') == True
vcheck('john', 'gameserver.start.date') == True
vcheck('john', 'gameserver.start.foobar') == True
```

`john` is too powerful we cant stop him now!

```python
vcheck('john', '**')
# Then
vcheck('john', 'anything') == True
```

<br>

## Installation
Using `pip`
```bash
pip install quickperms
```
Using `uv`
```bash
uv add quickperms
```

<br>

## Configuration
Quickperms uses environment variables to get database info.

| Environment Variable  | Type | Acceptable Values     |
| --------------------- | ---- | --------------------- |
| VALKEY_HOST           | str  | `localhost`or`valkey://valkey-container`or`https://example.com/valkey-db` |
| VALKEY_PORT           | int  | `6379`                |
| VALKEY_DB             | int  | `0` or may be 0-15    |
| VALKEY_PASS           | str  | unset or`password`    |

<br>

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
`vset(uid: str, permission: str, **kwargs) -> bool`

`uid`: str = Any string

`permission`: str = Any string seperated by `.`

__**optional \*\*kwargs**__

`glob`: str = Character to replace `*` with in the database. This defaults to `&`

---

`vcheck(uid: str, permission: str, **kwargs) -> bool`

`uid`: str = Any string

`permission`: str = Any string seperated by `.`

__**optional \*\*kwargs**__

`glob`: str = Character to replace `*` with in the database. This defaults to `&`
