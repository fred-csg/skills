"""Lápis Vivo — cria a pasta de um projeto novo com tudo que o index.html precisa.

uso: python -I novo_projeto.py <pasta_projeto>

Copia index.html, lv.css, lv.js, doodles.js e assets/ (fontes). Cria roteiro.js a partir do exemplo
se ainda não existir. Pode rodar de novo pra atualizar o motor sem mexer no roteiro.
"""
import os, shutil, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(AQUI)
dst = sys.argv[1]
os.makedirs(dst, exist_ok=True)
for f in ("index.html", "lv.css", "lv.js", "doodles.js"):
    shutil.copy2(os.path.join(AQUI, f), dst)
a_src, a_dst = os.path.join(SKILL, "assets"), os.path.join(dst, "assets")
os.makedirs(a_dst, exist_ok=True)
for f in os.listdir(a_src):
    s = os.path.join(a_src, f)
    if f == "sfx": continue
    if os.path.isdir(s): shutil.copytree(s, os.path.join(a_dst, f), dirs_exist_ok=True)
    else: shutil.copy2(s, a_dst)
r = os.path.join(dst, "roteiro.js")
if not os.path.exists(r): shutil.copy2(os.path.join(AQUI, "roteiro_exemplo.js"), r)
print("ok", dst)
