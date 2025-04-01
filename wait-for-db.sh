#!/bin/sh

until pg_isready -h db -U ${POSTGRES_USER} -d ${POSTGRES_DB}; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done