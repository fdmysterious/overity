Contributing
============

Suggest a new feature
---------------------

If you like to see a new feature, feel free to open an issue. We shall look if it can be planned on an upcoming version if it matches the scheduled roadmap.

Submitting code changes
-----------------------

Submitting code changes follow the usual procedure:

1. Fork the repo
2. Make your changes
3. Make sure your changes follow the required code rules and format, more info below
4. Submit a PR

Please make sure to attach your PR with an existing issue, or create a new one.


Development
-----------

### Tools

The project uses the following tools:

- `hatch`: project management, virtual environment, packaging tools;
- `pre-commit`: quality assurance for repo focusing on developer experience (DX).

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


### File header

Please use the following header format for source files:

```
[Main file title]
=================

**[Month] [year]**

- [Your Name] ([your email])

> This file is part of the Overity.ai project, and is licensed under
> the terms of the Apache 2.0 license. See the LICENSE file for more
> information.

Optional file description and documentation
```

Here is an example:

```
This file is here for this
==========================

**August 2025**

- John Doe (john.doe@mail.com)
```

You can omit your mail if you do not want to share it.
