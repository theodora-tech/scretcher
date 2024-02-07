install:
    poetry install

check:
  ruff .

fix:
  ruff . --fix