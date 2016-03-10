# python_logging
Common logging facility, for auditing purposes

## Dependecies

* PaYaml

## Usage

If you've already cloned a parent repo, populate the empty Python logging folder with:
```
git submodule update --init --recursive
```

To add to a new repo:

```git submodule add ../python_logging```

and (in a Python context) ...

```from python_logging.setup_logging import setup_logging```

## Design Notes

* See https://github.com/LandRegistry/python_logging/wiki#design-notes.
