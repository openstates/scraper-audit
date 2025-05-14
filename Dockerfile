FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONIOENCODING='utf-8'

# set the workdir directory to the environment so bash can find it
ENV WORKDIR='/app'
WORKDIR /app

# disable virtualenv creation to help save some space and slightly speedup startup
RUN apt-get update -qq \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y -qq --no-install-recommends \
  && pip install --disable-pip-version-check --no-cache-dir -q wheel \
  && pip install --disable-pip-version-check --no-cache-dir -q poetry crcmod \
  && poetry config virtualenvs.create false

# Copy poetry files
COPY pyproject.toml /app
COPY poetry.lock /app


# install dependencies before copying files in, this makes the install step *slightly* faster, and makes re-builds significantly faster
RUN poetry install --no-root \
    && rm -r /root/.cache/pypoetry/cache /root/.cache/pypoetry/artifacts/ \
    && apt-get remove -y -qq \
      build-essential \
      libpq-dev \
    && apt-get autoremove -y -qq \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy application code
COPY . /app

ENTRYPOINT ["poetry", "run", "python", "main.py"]
