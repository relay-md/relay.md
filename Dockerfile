FROM python:3.8-alpine3.15

# Copy over the requirements.txt file
COPY requirements.txt /requirements.txt

# Install system dependencies
RUN \
    apk add --no-cache --virtual .build-deps \
        build-base \
        musl-dev \
        libffi-dev \
        libressl-dev \
        openssl-dev \
        libxml2-dev \
        libxslt-dev \
        libgcc \
        openssl-dev \
    && apk add --no-cache \
        python3-dev \
        git \
        curl \
        bash \
        wget \
        gettext \
        mariadb-connector-c-dev \
    && CRYPTOGRAPHY_DONT_BUILD_RUST=1 pip3 install --no-cache-dir -r /requirements.txt \
    && apk del .build-deps

# Install app
COPY . /app

# Define $HOME
ENV HOME /app

# Working dir inside the app
WORKDIR /app

# Expose port 5000 for uvicorn
EXPOSE 5000

# Creates a non-root user and adds permission to access the /app folder
RUN    addgroup -S appgroup \
    && adduser -S appuser -G appgroup \
    && chown -R appuser /app
USER appuser

# Make settings persitent (https://stackoverflow.com/a/26145444/433627)
VOLUME ["/app"]

# Run API
ENTRYPOINT ["/app/entrypoint.sh"]
