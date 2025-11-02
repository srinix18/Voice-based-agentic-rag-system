#!/usr/bin/env python3
import json
import sys
import os

def load_env(path):
    """Load simple KEY=VALUE pairs from a .env file into os.environ if not already set."""
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            if k and v and k not in os.environ:
                os.environ[k] = v


try:
    from google import genai
except Exception as e:
    print("ERROR: couldn't import google.genai. Is the venv activated and the package installed?", file=sys.stderr)
    raise

# Try load .env from current folder (financial_rag_agent/.env) and repo root
load_env(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_env(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

client = genai.Client()

out = []
# The genai client has had multiple method names across versions. Try a few fallbacks.
models = None
errors = []
try:
    models = client.models.list()
except Exception as e:
    errors.append(f"client.models.list() -> {e}")
try:
    if models is None:
        models = client.list_models()
except Exception as e:
    errors.append(f"client.list_models() -> {e}")
try:
    if models is None:
        models = client.models.list_models()
except Exception as e:
    errors.append(f"client.models.list_models() -> {e}")
if models is None:
    print("Error while listing models, tried multiple methods:")
    for e in errors:
        print("  ", e, file=sys.stderr)
    raise RuntimeError("Could not list models using genai client - method not found in this SDK version")

for m in models:
    try:
        md = m.to_dict() if hasattr(m, "to_dict") else dict(m)
    except Exception:
        md = {"repr": str(m)}
    name = md.get("name") or md.get("id") or getattr(m, "name", None)
    supported = md.get("supported_methods") or md.get("supportedMethods") or md.get("supported_response_modalities") or md.get("supportedResponseModalities") or md.get("capabilities")
    out.append({"name": name, "supported": supported, "raw_keys": list(md.keys())[:20]})

out_path = os.path.join(os.path.dirname(__file__), '..', 'models_list.json')
out_path = os.path.abspath(out_path)
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(out, f, indent=2)

print(f"Wrote {out_path} with {len(out)} entries")
