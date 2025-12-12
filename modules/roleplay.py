import json
from pathlib import Path

PROMPT_PATH = Path("prompts/roleplay_system.txt")

def load_system_prompt() -> str:
    if not PROMPT_PATH.exists():
        raise FileNotFoundError(f"No existe {PROMPT_PATH}. Crealo y pegá el prompt ahí.")
    return PROMPT_PATH.read_text(encoding="utf-8")

def load_roleplay_payload(json_path: str) -> dict:
    p = Path(json_path)
    if not p.exists():
        raise FileNotFoundError(f"No existe {json_path}. Crealo con el JSON de ejemplo.")
    return json.loads(p.read_text(encoding="utf-8"))
