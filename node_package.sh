#!/bin/bash

packages=(
    "dora-keyboard==v0.3.7rc0"
    "opencv-python"
    "dora-qwenvl"
    "llama-factory-recorder"
    "dora-rerun"
    "rerun-sdk"
)

for package in "${packages[@]}"; do
    pip install "$package"
done
