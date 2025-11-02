#!/usr/bin/env python3
import json
import sys
try:
    from google import genai
except Exception as e:
    print("ERROR: couldn't import google.genai. Is the venv activated and the package installed?", file=sys.stderr)
    raise

client = genai.Client()

print("Listing available models (this may take a few seconds)...")
try:
    models = client.models.list_models()
except Exception as e:
    print("Error while listing models:", e, file=sys.stderr)
    raise

count = 0
for m in models:
    count += 1
    try:
        md = m.to_dict() if hasattr(m, "to_dict") else dict(m)
    except Exception:
        try:
            md = {"name": getattr(m, "name", str(m))}
        except Exception:
            md = {"repr": str(m)}

    name = md.get("name") or md.get("model") or getattr(m, "name", None)
    supported = md.get("supported_methods") or md.get("supportedMethods") or md.get("supported_response_modalities") or md.get("supportedResponseModalities") or md.get("supportedModalities") or md.get("capabilities")

    out = {"name": name, "supported": supported}
    # print truncated raw metadata for inspection
    out_raw = {k: md.get(k) for k in ("name", "description", "id", "id_", "display_name") if k in md}
    print(json.dumps({"model": out, "raw_sample": out_raw}, indent=2))

print(f"\nTotal models listed: {count}")
