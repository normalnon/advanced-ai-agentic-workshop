#!/bin/bash

echo "Installing workshop dependencies..."

pip install -r requirements.txt

playwright install

echo "Environment setup completed."
