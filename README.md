# Painel de Mineração de Ofertas

Painel estático (GitHub Pages). Os dados ficam em `data.enc.json`, criptografados (AES-GCM + PBKDF2); a página pede a senha para abrir.

Atualizado diariamente pela rotina de mineração: `python3 build.py export.json <senha>` gera o `data.enc.json`.
