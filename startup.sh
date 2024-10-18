#!/bin/bash

# Load environment variables
source .env

# Install Node.js dependencies
npm install

# Build the application
npm run build

# Start the application
npm run start