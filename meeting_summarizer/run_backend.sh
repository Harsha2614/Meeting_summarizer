#!/bin/bash
source .venv/bin/activate
uvicorn backend.app:app --reload --host 0.0.0.0 --port 8000
