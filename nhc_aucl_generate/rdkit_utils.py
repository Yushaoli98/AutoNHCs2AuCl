from rdkit import Chem
from rdkit.Chem import AllChem

def find_carbanion_carbon(mol):
    pattern = Chem.MolFromSmarts("[C-]")
    matches = mol.GetSubstructMatches(pattern)
    return [m[0] for m in matches]


def optimize_nhc(smiles, carbene_idx=None):
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    if carbene_idx is not None:
        rw = Chem.RWMol(mol)
        atom = rw.GetAtomWithIdx(carbene_idx)
        to_rm = [nbr.GetIdx() for nbr in atom.GetNeighbors() if nbr.GetSymbol() == 'H']
        for h in sorted(to_rm, reverse=True):
            rw.RemoveAtom(h)
        mol = rw.GetMol()

    AllChem.EmbedMolecule(mol, AllChem.ETKDGv3())
    return mol
