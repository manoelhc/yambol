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
  export OLLAMA_HOSTNAME=192.168.68.108
  export OLLAMA_PORT=11434
  export OLLAMA_PROTO=http
  python -m poetry run -- python -m yambol.app ../examples/user.yaml -o sql > SQL.sql
  #python -m poetry run -- python -m yambol.app ../examples/user.yaml -o debug > DEBUG.py
  #python -m poetry run -- python -m yambol.app ../examples/user.yaml -o mermaid > MERMAID.mermaid
  #python -m poetry run -- python -m yambol.app ../examples/user.yaml -o markdown