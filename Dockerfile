# --- Стадия сборки админки (React + consta) ---
FROM node:22-alpine AS admin-build

WORKDIR /admin

COPY admin/package.json admin/package-lock.json ./
RUN npm ci

COPY admin/ ./
RUN npm run build

# --- Стадия сборки приложения ---
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src
COPY icons ./icons
COPY database.db ./database.db
COPY entrypoint.sh /entrypoint.sh
COPY --from=admin-build /admin/dist ./admin-dist
RUN chmod +x /entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
