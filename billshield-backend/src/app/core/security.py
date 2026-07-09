from __future__ import annotations

import hashlib
import os
import secrets
import uuid
from pathlib import Path


def generate_uuid() -> str:
    return str(uuid.uuid4())


def generate_safe_filename(original_filename: str) -> str:
    name, ext = os.path.splitext(original_filename)
    ext = ext.lower()
    safe_name = "".join(c for c in name if c.isalnum() or c in "._-")[:100]
    token = secrets.token_hex(8)
    return f"{safe_name}_{token}{ext}"


def sanitize_path(base_dir: Path, filename: str) -> Path:
    resolved = (base_dir / filename).resolve()
    if not str(resolved).startswith(str(base_dir.resolve())):
        raise ValueError("Path traversal detected")
    return resolved


def hash_filename(filename: str) -> str:
    return hashlib.sha256(filename.encode()).hexdigest()[:16]
