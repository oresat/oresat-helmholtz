# Installing dev dependencies

```shell
$ python3 -m venv env
$ . env/bin/activate
$ pip install --user -e .[dev]
$ pytest
```

If all of these steps succeed, your environment is properly configured to develop this project.

# Before pushing

Run the following to lint your code before pushing your changes.
Note that this makes changes to your code in-place.

```shell
$ scripts/format.sh
```
