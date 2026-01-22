#!/bin/bash

# ShieldAgent Stop Script
# Run this script to stop both backend and frontend servers

echo "🛑 Stopping ShieldAgent..."

# Kill processes on ports
lsof -ti:8000 | xargs kill -9 2>/dev/null
lsof -ti:5173 | xargs kill -9 2>/dev/null

echo "✓ Services stopped"
