FROM python:3.8-slim

# Copy over the requirements.txt file
COPY requirements.txt /requirements.txt

# Install system dependencies
RUN apt-get update -y \
    && apt-get install --no-install-recommends -y \
        gcc \
        default-libmysqlclient-dev \
        python3.8-dev \
        python3-pip \
        nodejs npm \
        gettext-base \
        bash \
    && CRYPTOGRAPHY_DONT_BUILD_RUST=1 pip3 install --no-cache-dir -r /requirements.txt \
    && apt-get clean \
    && rm -rf /var/cache/apt /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Install app
COPY . /app

# Define $HOME
ENV HOME /app

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# Working dir inside the app
WORKDIR /app

# Node
RUN npm ci && npm run build

# Expose port 5000 for uvicorn
EXPOSE 5000

# Creates a non-root user and adds permission to access the /app folder
#
RUN    useradd --create-home appuser \
    && chown -R appuser /app
USER appuser

# Make settings persitent (https://stackoverflow.com/a/26145444/433627)
VOLUME ["/app"]

# Run API
ENTRYPOINT ["/app/entrypoint.sh"]
