"""Gera por código (sem biblioteca de sons) os efeitos que o vídeo usa: <projeto>/sfx/<id>.wav.

uso (na pasta do projeto, depois de exportar as cues):  python -I scripts/gerar_sfx.py out/cues.json
O mix-sfx.mjs usa a biblioteca do autor se existir no computador; senão pega estes arquivos.
Só gera o que ainda não existe em sfx/ (pode trocar qualquer um por um som seu, mesmo nome).
"""
import json, os, sys, wave
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfx_synth import synth, SR

RECEITA = {
    "Very Short Click_Camera": "click_short click_metal beep_tick mouse fut_blip glitchy_bleep msg_bleep app_open",
    "Single Click Shutter": "pop_soft snap_elastic",
    "Crispy Small Whoosh": "whip_a whip_b whip_c whip_d swipe_rl whoosh_exhale stutter_whoosh",
    "DSGNWhsh_Paper Whoosh": "swipe_paper swipe_sand",
    "Distorted Paper Whoosh": "reverse_swell riser_pulse riser_sparkle",
    "Camera Clicks, Low Impact, Mech Double Hit": "impact_soft impact_low final_hit sub_tail bass_mecha braam tonal_accent",
    "Multi Small Gear Rotation, Double Low Whoosh": "gears mech_lock servo_init",
    "Stopwatch Clicks_Cinematic": "ticking glitchy_counter tonal_beeps elec_ui",
    "Modern Minimize": "glitch glitch2 glitch3",
    "System Slowing Down": "robot_down",
    "Computer Keyboard Quick Typing": "typing",
    "UI Bright Chime": "chime bursting_bleep",
}
ID2NOME = {i: nome for nome, ids in RECEITA.items() for i in ids.split()}

cues = json.load(open(sys.argv[1], encoding="utf8"))["cues"]
os.makedirs("sfx", exist_ok=True)
feitos = 0
for i in sorted({c["id"] for c in cues}):
    dst = os.path.join("sfx", f"{i}.wav")
    if os.path.exists(dst) or os.path.exists(dst[:-4] + ".mp3"): continue
    a = np.clip(synth(ID2NOME.get(i, "Very Short Click_Camera")), -1, 1)
    w = wave.open(dst, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((a * 32767).astype("<i2").tobytes()); w.close(); feitos += 1
print(f"{feitos} sons gerados em sfx/")
