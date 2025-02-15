c_env := "python3 -m venv .venv; source .venv/bin/activate;"

setup:
  #!/bin/bash
  {{ c_env }}
  pip install poetry
  pip install --upgrade pip

run:
  #!/bin/bash
  {{ c_env }}
  cd yambol
  python -m poetry run -- python -m yambol.app ../examples/user.yaml