# Overity.ai python

- Florian Dupeyron <florian.dupeyron@elsys-design.com>
- December 2024

Overity.ai python toolkit


## Development

### Tools

The project uses the following tools:

- hatch: project management, virtual environment, packaging tools;
- pre-commit: quality assurance for repo focusing on developer experience (DX).

You can install these tools (one time only) using pip:

```
pip install hatch pre-commit
```

The first time you checkout the repository, make sure to configure `pre-commit` properly:

```
pre-commit install
```

### Environments

This project makes an extensive use of hatch's "environments" fulfilling various needs:

#### `docs` environment

This environment allow to build the project's documentation using `mkdocs`. To build the project documentation, simply run:

```
hatch run docs:build
```

Generated documentation shall be available in the `site` output folder.


#### `types` environment

This auxiliary environment uses `mypy` for type checking.

You can run the type checker using:

```
hatch run types:check
```


#### `lint` environment

This environment contains the `ruff` linter as well as the `black` formatter. These shall be already run by `pre-commit` when comitting to the repository.

Behind the scenes, the `pre-commit` hooks makes use of the following commands:

- Lint the code using `ruff`: `hatch run lint:code-rules`
- Format the code using `black`: `hatch run lint:code-format`
