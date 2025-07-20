#!/bin/bash

echo "✅ Starting Backend API..."
uvicorn main:app --host 0.0.0.0 --port 5000 &

echo "🤖 Starting Discord Bot..."
python discord_bot.py
