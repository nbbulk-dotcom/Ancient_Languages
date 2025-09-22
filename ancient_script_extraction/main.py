import os
import yaml
from scripts.linear_a.extractor_linear_a import run_linear_a_extraction
from scripts.khitan.extractor_khitan import run_khitan_extraction
from scripts.proto_elamite.extractor_proto_elamite import run_proto_elamite_extraction
from scripts.indus.extractor_indus import run_indus_extraction

def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def main():
    config = load_config('config.yaml')
    outdir = config.get('output_dir', './output')
    os.makedirs(outdir, exist_ok=True)

    print("Running Linear A extraction...")
    run_linear_a_extraction(config, outdir)

    print("Running Khitan Large Script extraction...")
    run_khitan_extraction(config, outdir)

    print("Running Proto-Elamite extraction...")
    run_proto_elamite_extraction(config, outdir)

    print("Running Indus Valley Script extraction...")
    run_indus_extraction(config, outdir)

    print("All extractions complete!")

if __name__ == "__main__":
    main()
