#!/bin/bash

export APP_RUN=${APP_RUN:=api}
export LOG_LEVEL=${APP_LOGLEVEL:=critical}

export FORWARDED_ALLOW_IPS=${FORWARDED_ALLOW_IPS:="*"}

function setup() {
	echo "Upgrading SQL Database Scheme:"
	alembic upgrade head
}

setup

COMMAND=$1
if [[ ! -z "$COMMAND" ]]; then
	shift
fi

case "$COMMAND" in
worker)
	echo "Launching Worker:"
	exec python3 main.py worker --identifier ${WORKER_IDENTIFIER:=general} --queue ${WORKER_QUEUES:=celery} --concurrency ${WORKER_CONCURRENCY:=1} $*
	;;

flower)
	echo "Launching Flower:"
	exec celery -A api.tasks.celery flower --address=${APP_HOST:="0.0.0.0"} --port=${APP_PORT:=5000} $*
	;;

beat)
	echo "Launching Beat:"
	exec celery -A api.tasks.celery beat $*
	;;

# Default
*)
	echo "Public API:"
	exec uvicorn api.api:app --host ${APP_HOST:="0.0.0.0"} --port ${APP_PORT:=5000} --log-level $LOG_LEVEL --proxy-headers $*
	;;

esac
