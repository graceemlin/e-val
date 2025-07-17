# E-Val
Small tool to generate SGF files out of KataGo variations 

## Setup
Clone this repository and init the submodules
```
git submodule update --init --recursive
```

Download the latest KataGo release and unzip it into a directory called 'katago_bin' to make the default CLI options line up

Download a KataGo model and put it somewhere

Potentially need to install missing PyPy packages:
- sgfmill
- tqdm

You can tweak the configuration or which model is being used via the command line options

## Usage
```
python3 e-val.py -h
usage: E-Val [-h] [-r {japanese,chinese,chinese-ogs,chinese-kgs,tromp-taylor,korean,stone-scoring,aga,bga}] [-k KATAGO] [-a ANALYSIS_CONFIG] [-m MODEL] [-o OUTDIR] sgf_file move [move ...]

Generates SGFs with variations from base SGF and list of moves to generate for

positional arguments:
  sgf_file              SGF file to analyze
  move                  One or more move numbers to analyse, note that in handicap games the handicap stones might not be considered a move

options:
  -h, --help            Show this help message and exit
  -r {japanese,chinese,chinese-ogs,chinese-kgs,tromp-taylor,korean,stone-scoring,aga,bga}, --rules {japanese,chinese,chinese-ogs,chinese-kgs,tromp-taylor,korean,stone-scoring,aga,bga}
  -k KATAGO, --katago KATAGO
                        Path to KataGo executable (default: ./katago_bin/katago)
  -a ANALYSIS_CONFIG, --analysis-config ANALYSIS_CONFIG
                        Path to analysis config file for KataGo (default: ./katago_bin/analysis_example.cfg)
  -m MODEL, --model MODEL
                        Path to KataGo model to use (default: ./katago_bin/g170-b30c320x2-s4824661760-d1229536699.bin.gz)
  -o OUTDIR, --outDir OUTDIR
                        Directory to write generated sgf files to (default: .)
```

The tool will generate a new SGF file for every move it was asked to generate variations for.\
If no output directory is specified it will generate them in the current directory.
