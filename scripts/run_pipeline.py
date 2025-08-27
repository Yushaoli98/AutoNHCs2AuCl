import argparse
from nhc_aucl_generate.pipeline import run_pipeline

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True, help="Input CSV file with SMILES")
    args = parser.parse_args()
    run_pipeline(args.csv)

if __name__ == "__main__":
    main()
