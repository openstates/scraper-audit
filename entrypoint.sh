#!/usr/bin/env bash
set -e

# Handle GCP credentials
if [[ -n "${GOOGLE_APPLICATION_CREDENTIALS}" ]]; then
    echo "Applying app credentials..."
    echo "${GOOGLE_APPLICATION_CREDENTIALS}" > /creds.json
    export GOOGLE_APPLICATION_CREDENTIALS="/creds.json"
elif [[ -n "${GOOGLE_CREDENTIAL_FILE}" ]]; then
    echo "Assuming a valid credentials file is mounted at ${GOOGLE_CREDENTIAL_FILE}..."
    export GOOGLE_APPLICATION_CREDENTIALS=${GOOGLE_CREDENTIAL_FILE}
fi

# Run the main app
exec poetry run python main.py "$@"
