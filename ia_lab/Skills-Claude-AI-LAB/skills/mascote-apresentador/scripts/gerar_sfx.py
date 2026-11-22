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
    "Very Short Click_Camera": "m_click m_mec m_shutter m_glitch click_short click_metal beep_tick mouse fut_blip glitchy_bleep msg_bleep app_open ui_click ui_click2 mec_click obturador",
    "Single Click Shutter": "m_popt m_pop m_plop m_bubble pop_soft snap_elastic ui_pop ui_pop2",
    "Crispy Small Whoosh": "m_whip m_swish m_ghost m_morph m_magic whip_a whip_b whip_c whip_d swipe_rl whoosh_exhale stutter_whoosh ui_swish ui_swish2 ui_whoosh",
    "DSGNWhsh_Paper Whoosh": "m_paper m_cloth m_clap swipe_paper swipe_sand",
    "Distorted Paper Whoosh": "reverse_swell riser_pulse riser_sparkle",
    "Camera Clicks, Low Impact, Mech Double Hit": "m_build m_build1 m_assemble m_hit m_impact m_spawn impact_soft impact_low final_hit sub_tail bass_mecha braam tonal_accent ui_impact ui_impact2",
    "Multi Small Gear Rotation, Double Low Whoosh": "m_catraca m_inventory gears mech_lock servo_init mec_catraca",
    "Stopwatch Clicks_Cinematic": "m_rajada m_timer ticking glitchy_counter tonal_beeps elec_ui",
    "Modern Minimize": "glitch glitch2 glitch3",
    "System Slowing Down": "robot_down",
    "Computer Keyboard Quick Typing": "typing",
    "UI Bright Chime": "m_bell m_sparkle m_coins m_cash chime bursting_bleep",
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
