# Digital Living Standards repository

This repository contains Base Data Standards by Digital Living.

Specification for describing data product standards can be found in
[draft/DataProducts/README.md](draft/DataProducts/README.md).

_Please note that this repository is under active development, and all the standards are
subjects to change at any time._

## Contribution guidelines

We accept contributions to this repository via
[Pull Requests](https://github.com/digitalliving/standards/pulls). You can fork the
repository, make your suggested changes in there, and then submit a Pull Request via
GitHub.

Before you submit a PR, please check that you follow these guidelines though to avoid
unnecessary work for everyone:

1. Install the following pre-requisites:
   - [Python 3.9](https://www.python.org/downloads/)
   - [poetry](https://python-poetry.org/docs/#installation) and all the python
     dependencies for this project (run `poetry install` to install them)
   - [pre-commit](https://pre-commit.com/#install) and make it active in your local
     clone (`pre-commit install` in repo root). Ensure this is in place BEFORE you make
     any changes, or later run `pre-commit run --all-files`.
2. Ensure your committed code follows the style guide configured in the repository
   (handled automatically by `pre-commit`)
3. Check that your naming follows existing standards. E.g. for JSON keys in Data Product
   we use `camelCase` always, do not try to submit new standards using `snake_case`.
4. Ensure you're submitting new things, i.e. check if there is an existing Data Product
   that already fits the use-case.
5. Breaking changes should be introduced via `draft`. If you want to add anything new,
   or propose a change to an existing standard that could break backwards compatibility,
   you should submit the changes in the `draft` version. Afterwards we can figure out
   which release version they can go in.

### Adding new Data Product Standards

There are two ways of contribution:

1. **Submit OpenAPI spec directly**

   For example, to add a definition for `Foo/Bar`:

   - create `draft/DataProducts/Foo/Bar.json`
   - make sure you follow the data product standard
     [guidelines](draft/DataProducts/README.md)

2. **Submit standard as python file**

   If you're familiar with python and
   [pydantic](https://github.com/samuelcolvin/pydantic) library, you may find it easier
   to create the standard as a set of pydantic models.

   For example, to add a definition for `Foo/Bar`:

   - create `src/draft/DataProducts/Foo/Bar.py`
   - run `pre-commit` to automatically convert it to OpenAPI spec and validate it

#### Data Product Standards as python files

Each data product standard represented as python file must define a `STANDARD` variable
which is an instance of `DataProductStandard` class. Please check existing examples in
[src/draft/DataProducts](src/draft/DataProducts).

DataProductStandard is a structure consisting of:

- `summary`

  Summary used in top of OpenAPI spec

- `description`

  Data product description, used in top of OpenAPI spec

- `request`

  pydantic model describing body of POST request

- `response`

  pydantic model describing expected response from data source

- `route_summary`

  Summary for the POST route

- `route_description`

  Description for the POST route

- `generic_description`

  You may omit providing `summary`, `description`, `route_summary` and
  `route_description` if you define this field. Others will be generated automatically
  based on it. Use something brief and meaningful, like "Company Recommendations" or
  "Cargo receipt".

### Data Product Standards validation

You can run the automatic validations also via Docker locally using the
`Dockerfile.validate` -configuration:

```bash
docker build . -f Dockerfile.validate
```

or by running pre-commit hooks:

```bash
pre-commit
```
