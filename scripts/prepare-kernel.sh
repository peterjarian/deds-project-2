#!/bin/bash

echo "Installing dependencies..."
poetry install

echo "Installing Jupyter kernel..."
poetry run python -m ipykernel install --user --name=myenv --display-name "Python (myenv)"

echo "Done preparing Dev Container, ready for use."
