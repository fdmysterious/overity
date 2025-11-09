# Development Commands

This file documents the commands used for development tasks in the Overity.ai project.

## Type Checking
- `hatch run types:check`: Run mypy for type checking.

## Linting and Formatting
- `hatch run lint:code-rules`: Lint the code using ruff.
- `hatch run lint:code-format`: Format the code using black.

## Documentation
- `hatch run docs:build`: Build the project documentation using mkdocs.

## Project Structure

The `src/overity` folder contains the following subfolders:

- `api`: API definition that can be used in overity methods
- `backend`: Internal operations
- `bench`: Bench abstraction definition
- `exchange`: Exchange file parsers and encoders
- `frontend`: CLI related code
- `model`: Data structures (especially dataclasses) definition
- `storage`: Storage abstractions definition

## Testing

Test code is available in the `tests` folder

To run tests, use the `hatch test -vv --cover` command
