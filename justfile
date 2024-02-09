# install (python) dependencies
install:
  poetry install

# check code style
check:
  ruff .

# fix/format code style
fix:
  ruff . --fix

# generate json schema from the data files
generate-data-schema:
