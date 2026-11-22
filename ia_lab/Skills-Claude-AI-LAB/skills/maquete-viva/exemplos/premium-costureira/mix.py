import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts", "molde"))  # no projeto: "../../lib"
import mvm
D = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "audio")
L = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "scripts", "molde", "sfx") + "/"
cues = [(L + "pop.mp3", 1.0, -13, "onset"), (L + "whoosh.mp3", 4.4, -13, "peak"), ("sfx/maquina.mp3", 4.9, -14, "start", 3.0)]
cues += [(L + "titulo.mp3", t + 0.05, -12, "onset") for t in (3.34, 5.72, 15.64, 23.56, 29.12)]
cues += [(L + "porta.mp3", 8.3, -14, "onset"), (L + "pop.mp3", 9.72, -14, "onset"), (L + "pop.mp3", 11.32, -14, "onset"),
         ("sfx/lapis.mp3", 12.48, -11, "start"), ("sfx/confusao.mp3", 13.62, -10, "onset"), (L + "whoosh.mp3", 15.9, -13, "peak"),
         (L + "foto.mp3", 18.1, -9, "peak"), ("sfx/toques.mp3", 20.1, -11, "start"), (L + "pop.mp3", 22.38, -11, "onset"),
         (L + "whoosh.mp3", 23.9, -14, "peak")]
cues += [(L + "pop.mp3", 24.06 + i * 0.25, -16, "onset") for i in range(4)]
cues += [(L + "pop.mp3", 26.26, -13, "onset"), (L + "celular.mp3", 27.38, -10, "start"), ("sfx/maquina.mp3", 29.2, -15, "start", 2.6),
         (L + "titulo.mp3", 31.1, -10, "onset"), (L + "pop.mp3", 32.94, -13, "onset"), (L + "pop.mp3", 34.42, -13, "onset"),
         (L + "whoosh.mp3", 36.26, -13, "peak"), (L + "redes.mp3", 40.0, -9, "start")]
mvm.mix(os.path.join(D, "locucao.mp3"), os.path.join(D, "trilha.mp3"), cues, 44.6, sys.argv[1], D)
