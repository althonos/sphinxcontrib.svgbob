# Contributing to `sphinxcontrib-svgbob`

For bug fixes or new features, please file an issue before submitting a
pull request. If the change isn't trivial, it may be best to wait for
feedback.

## Setting up a local repository

You can just clone the repository without needing any extra setup to get a
local copy of the code:

```console
$ git clone https://github.com/althonos/sphinxcontrib-svgbob
```

## Running tests

Tests are written as usual Python unit tests with the `unittest` module of
the standard library. Running them requires the extension to be built
locally:

```console
$ python -m pip install --no-build-isolation -e . -v
$ python -m unittest sphinxcontrib.svgbob.tests -vv
```

## Coding guidelines

This project targets Python 3.7 or later.

### Type hints

Python objects should be typed where applicable. For the Rust code,
an external type stub must be maintained; if the `to_svg` arguments
are changed, or new arguments are added, make sure to update `_svgbob.pyi`
as well.

### Interfacing with Rust

This project uses Rust and [`pyo3`](https://pyo3.rs) to interface with the
`svgbob` code. You'll need a Rust compiler on your system to compile the
extension if you are going to tinker with the code, even if you only intend
to edit the Python part of the code.

If you're unfamiliar with Rust, check the [*Get Started*](https://www.rust-lang.org/learn/get-started)
page of the Rust documentation on how to get a local toolchain.
