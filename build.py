#!/usr/bin/env python3
"""Gera data.enc.json (AES-GCM + PBKDF2) para o painel estático.

Uso: python3 build.py export.json SENHA [saida=data.enc.json]
export.json = {"ofertas":[...], "execucao":{...}, "analise":{...}}
"""
import base64, json, os, sys
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ITER = 200_000

def main():
    src, pw = sys.argv[1], sys.argv[2]
    out = sys.argv[3] if len(sys.argv) > 3 else "data.enc.json"
    data = json.load(open(src, encoding="utf-8"))
    # nunca publicar ofertas descartadas nem campos internos
    data["ofertas"] = [o for o in data.get("ofertas", []) if o.get("marcacao") != "desc"]
    salt, iv = os.urandom(16), os.urandom(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(pw.encode())
    ct = AESGCM(key).encrypt(iv, json.dumps(data, ensure_ascii=False).encode(), None)
    b = lambda x: base64.b64encode(x).decode()
    json.dump({"v": 1, "iter": ITER, "salt": b(salt), "iv": b(iv), "ct": b(ct)}, open(out, "w"))
    print(f"ok: {len(data['ofertas'])} ofertas -> {out}")

if __name__ == "__main__":
    main()
