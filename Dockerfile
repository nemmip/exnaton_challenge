FROM python:3.11 AS base

# Etap backend
FROM base AS backend

ENV VIRTUAL_ENV=/exnaton_challenge/.venv
ENV PYTHONDONTWRITEBYTECODE=1
ENV POETRY_NO_INTERACTION=1
ENV POETRY_CACHE_DIR=/tmp/poetry_cache
ENV DATABASE_URL=0.0.0.0:5433

WORKDIR /exnaton_challenge/backend
COPY backend/pyproject.toml backend/poetry.lock ./

RUN pip install --upgrade poetry virtualenv \
    && virtualenv ${VIRTUAL_ENV} --python=python3.11 \
    && . ${VIRTUAL_ENV}/bin/activate \
    && poetry install --no-root --only main \
    && rm -rf ${POETRY_CACHE_DIR}

# Etap frontend
FROM base AS frontend

ENV NODE_ENV=$ENV
ENV NODE_VERSION=v20.15.1
ENV NVM_DIR=/usr/local/nvm

WORKDIR /exnaton_challenge/frontend
COPY frontend/ ./

RUN curl -o /tmp/install.sh https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh \
    && mkdir ${NVM_DIR} && bash /tmp/install.sh && . ${NVM_DIR}/nvm.sh \
    && nvm install ${NODE_VERSION} && nvm alias default ${NODE_VERSION} && nvm use default \
    && npm install -g npm@latest

ENV NODE_PATH=${NVM_DIR}/$NODE_VERSION/lib/node_modules
ENV PATH=${NVM_DIR}/versions/node/${NODE_VERSION}/bin:$PATH

RUN npm clean-install --include=dev \
    && npm cache clean --force \
    && npm run build:prod

# Etap runtime
FROM base AS runtime

WORKDIR /exnaton_challenge
COPY --from=backend /exnaton_challenge/backend ./
COPY --from=backend /exnaton_challenge/.venv .venv
COPY --from=frontend /exnaton_challenge/frontend/dist ./frontend/dist

ENV PYTHONPATH=/exnaton_challenge/backend
ENV PATH=/exnaton_challenge/.venv/bin:$PATH

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
