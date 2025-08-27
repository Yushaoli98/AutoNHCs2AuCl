import os
import pandas as pd
from concurrent.futures import ProcessPoolExecutor, as_completed
from .io_utils import write_xyz, read_xyz, save_failed
from .rdkit_utils import find_carbanion_carbon, optimize_nhc
from .crest_utils import run_crest
from .xtb_utils import optimize_with_xtb
from .geometry_utils import select_best_direction, generate_aucl
from .config import OUTPUT_DIR, FAILED_CSV, USE_HALF_CORES


MAX_WORKERS = os.cpu_count() // 2 if USE_HALF_CORES else os.cpu_count()

def process_row(row):
    mol_id = row.get('ID')
    smi = row.get('Processed_SMILES') or row.get('Original_SMILES')
    try:
        mol_nhc = optimize_nhc(smi)
        elems_nhc = [a.GetSymbol() for a in mol_nhc.GetAtoms()]
        coords_nhc = [[a.GetOwningMol().GetConformer().GetAtomPosition(i).x,
                       a.GetOwningMol().GetConformer().GetAtomPosition(i).y,
                       a.GetOwningMol().GetConformer().GetAtomPosition(i).z]
                       for i,a in enumerate(mol_nhc.GetAtoms())]
        nhc_path = os.path.join(OUTPUT_DIR, f"{mol_id}_nhc.xyz")
        write_xyz(nhc_path, elems_nhc, coords_nhc)
        crest_dir = os.path.join(OUTPUT_DIR, f"{mol_id}_crest")
        crest_best = run_crest(nhc_path, crest_dir)
        elems_best, coords_best = read_xyz(crest_best)
        carb_idx = find_carbanion_carbon(mol_nhc)[0]
        carb_xyz = coords_best[carb_idx]
        direction = select_best_direction(carb_xyz, coords_best)
        au_elems, au_coords = generate_aucl(carb_xyz, direction)
        all_elems = elems_best + au_elems
        import numpy as np
        all_coords = np.vstack([coords_best, au_coords])
        raw_path = os.path.join(OUTPUT_DIR, f"{mol_id}.xyz")
        write_xyz(raw_path, all_elems, all_coords)
        opt_path = os.path.join(OUTPUT_DIR, f"{mol_id}_opt.xyz")
        optimize_with_xtb(raw_path, opt_path)
        return None
    except Exception as e:
        return {"ID": mol_id, "SMILES": smi, "Error": str(e)}

def run_pipeline(csv_file):
    df = pd.read_csv(csv_file, dtype=str).dropna(subset=['ID'])
    failed = []
    with ProcessPoolExecutor(max_workers=MAX_WORKERS) as ex:
        futures = [ex.submit(process_row, row._asdict()) for row in df.itertuples(index=False)]
        for fut in as_completed(futures):
            res = fut.result()
            if res: failed.append(res)
    save_failed(failed, FAILED_CSV)
