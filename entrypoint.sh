#!/bin/sh
set -e

# БД приходит из образа или из bind-mount (локальная database.db). seed — только
# страховка на случай, если файл отсутствует или пуст (например, docker создал
# пустой файл при монтировании), т.к. seed.py пересоздаёт таблицы
# (drop_all + create_all) и генерирует новые api_key.
if [ ! -s database.db ]; then
    echo "[entrypoint] database.db не найден — заполняю БД заново..."
    python -m src.seed
fi

exec uvicorn src.main:app --host 0.0.0.0 --port "${PORT:-8000}"
