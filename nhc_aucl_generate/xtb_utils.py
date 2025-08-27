import os, subprocess, shutil
from .config import XTB_EXECUTABLE


def optimize_with_xtb(in_xyz, out_xyz):
    workdir = os.path.dirname(out_xyz)
    base = os.path.splitext(os.path.basename(out_xyz))[0]
    tmp_in = os.path.join(workdir, base + "_xtb_in.xyz")
    shutil.copy(in_xyz, tmp_in)
    cmd = [XTB_EXECUTABLE, os.path.basename(tmp_in), "--opt", "--chrg", "0", "--gfn", "2"]
    env = os.environ.copy()
    env["OMP_NUM_THREADS"] = "1"
    res = subprocess.run(cmd, cwd=workdir, env=env, capture_output=True, text=True)
    final_out = os.path.join(workdir, "xtbopt.xyz")
    if os.path.exists(final_out):
        shutil.move(final_out, out_xyz)
    else:
        raise RuntimeError("XTB optimization failed")
