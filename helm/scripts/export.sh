#!/bin/bash
STARTING_DIR="$(pwd)"
HELM_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && cd ../ && pwd)"

ENVIRONMENT=dev
if [ -n "$1" ]; then
  ENVIRONMENT=$1
fi

# platform default is cats
PLATFORM="-cats"
if [ -n "$2" ]; then
  PLATFORM="-$2"
fi

# if the platform is not cats or kubed, then throw error
if [ "$PLATFORM" != "-cats" ] && [ "$PLATFORM" != "-kubed" ]; then
  echo "Invalid platform. Available platforms include local, Lilly CATS or Lilly Kubed"
  exit 1
fi

VALUES_FILE=$HELM_DIR/values$PLATFORM.$ENVIRONMENT.yaml
if [ "$ENVIRONMENT" == "local" ]; then
  VALUES_FILE=$HELM_DIR/values.yaml
fi

echo "Exporting helm chart for $ENVIRONMENT environment"
echo "Using values file: $VALUES_FILE"

helm template -g $HELM_DIR --output-dir $HELM_DIR -f $VALUES_FILE --debug