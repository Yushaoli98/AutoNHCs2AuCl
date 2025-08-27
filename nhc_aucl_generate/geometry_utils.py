import numpy as np
from scipy.spatial import KDTree
from .config import AU_C_DIST, CL_DIST, NUM_DIRS


def select_best_direction(carb_xyz, coords):
    n = NUM_DIRS
    idx = np.arange(0, n, dtype=float) + 0.5
    phi = np.arccos(1 - 2 * idx / n)
    theta = np.pi * (1 + 5**0.5) * idx
    dirs = np.vstack([np.cos(theta) * np.sin(phi),
                      np.sin(theta) * np.sin(phi),
                      np.cos(phi)]).T
    dists = np.linalg.norm(coords - carb_xyz, axis=1)
    nbrs = np.argsort(dists)[1:3]
    v1, v2 = coords[nbrs[0]] - carb_xyz, coords[nbrs[1]] - carb_xyz
    normal = np.cross(v1, v2)
    normal = normal / (np.linalg.norm(normal) + 1e-8)
    tree = KDTree(coords)
    best_u, best_score = normal, -1.0
    for u in dirs:
        dot = float(np.clip(np.dot(u, normal), -1.0, 1.0))
        ang = np.degrees(np.arccos(dot))
        if abs(ang) > 60: continue
        au_pos = carb_xyz + u * AU_C_DIST
        cl_pos = au_pos + u * CL_DIST
        d_au, _ = tree.query(au_pos, k=2)
        d_cl, _ = tree.query(cl_pos, k=1)
        min_d = min(d_au[0] if np.ndim(d_au) else d_au, d_cl)
        if min_d > best_score:
            best_score, best_u = min_d, u
    return best_u

def generate_aucl(carb_xyz, direction):
    u = direction / max(1e-12, np.linalg.norm(direction))
    au = carb_xyz + u * AU_C_DIST
    cl = au + u * CL_DIST
    return ['Au', 'Cl'], np.vstack([au, cl])
