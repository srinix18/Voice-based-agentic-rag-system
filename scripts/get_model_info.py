#!/usr/bin/env python3
import json
import os
import sys

# Load .env if present
def load_env(path):
    if not os.path.exists(path):
        return
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k,v=line.split('=',1)
            k=k.strip(); v=v.strip().strip('"').strip("'")
            if k and v and k not in os.environ:
                os.environ[k]=v

load_env(os.path.join(os.path.dirname(__file__), '..', '.env'))
load_env(os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env'))

try:
    from google import genai
except Exception as e:
    print('ERROR: cannot import google.genai - ensure venv is activated and package installed', file=sys.stderr)
    raise

client = genai.Client()
model_name = 'models/gemini-2.0-flash-live-001'

result = None
errors = []
# Try several method names depending on SDK version
try:
    # newer SDK might have client.models.get(name)
    if hasattr(client, 'models') and hasattr(client.models, 'get'):
        # different SDKs have varying signatures. Try keyword 'model' first.
        try:
            result = client.models.get(model=model_name)
        except TypeError as e:
            try:
                # maybe positional required
                result = client.models.get(model_name)
            except Exception:
                # fallback: client.models.get() may return iterable; try scanning
                try:
                    all_models = client.models.get()
                    for m in all_models:
                        if (getattr(m, 'name', None) == model_name) or (isinstance(m, dict) and m.get('name') == model_name):
                            result = m
                            break
                except Exception:
                    pass
except Exception as e:
    errors.append(f'client.models.get -> {e}')

try:
    if result is None and hasattr(client, 'get_model'):
        result = client.get_model(model_name)
except Exception as e:
    errors.append(f'client.get_model -> {e}')

try:
    if result is None and hasattr(client, 'models') and hasattr(client.models, 'get_model'):
        result = client.models.get_model(model_name)
except Exception as e:
    errors.append(f'client.models.get_model -> {e}')

try:
    if result is None and hasattr(client, 'models') and hasattr(client.models, 'describe'):
        result = client.models.describe(model_name)
except Exception as e:
    errors.append(f'client.models.describe -> {e}')

if result is None:
    print('All attempts failed to fetch model. Errors:')
    for e in errors:
        print('  ', e, file=sys.stderr)
    sys.exit(2)

def to_primitive(o):
    # Recursively convert SDK objects to JSON-serializable primitives
    if o is None:
        return None
    if isinstance(o, (str, int, float, bool)):
        return o
    if isinstance(o, list):
        return [to_primitive(i) for i in o]
    if isinstance(o, dict):
        return {k: to_primitive(v) for k, v in o.items()}
    if hasattr(o, 'to_dict'):
        try:
            return to_primitive(o.to_dict())
        except Exception:
            pass
    if hasattr(o, '__dict__'):
        try:
            return to_primitive(vars(o))
        except Exception:
            pass
    # Fallback to string representation
    try:
        return str(o)
    except Exception:
        return repr(o)

# Convert to JSON-serializable structure
md = to_primitive(result)

out_path = os.path.join(os.path.dirname(__file__), '..', 'model_gemini-2.0-flash-live-001.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(md, f, indent=2)

print('Wrote', out_path)
