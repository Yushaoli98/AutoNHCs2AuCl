import os, subprocess, shutil
from .config import CREST_EXECUTABLE, TEMPERATURE, GFIN_METHOD


def run_crest(in_xyz, workdir, temp_k=298, gfn="2", quick=False):
    os.makedirs(workdir, exist_ok=True)
    inp = os.path.join(workdir, "crest_inp.xyz")
    shutil.copy(in_xyz, inp)
    cmd = [CREST_EXECUTABLE, os.path.basename(inp), f"--gfn{gfn}", "--T", str(temp_k)]
    if quick:
        cmd.append("--quick")
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    res = subprocess.run(cmd, cwd=workdir, env=env, capture_output=True, text=True)
    best = os.path.join(workdir, "crest_best.xyz")
    if not os.path.exists(best):
        raise RuntimeError("CREST failed")
    return best
