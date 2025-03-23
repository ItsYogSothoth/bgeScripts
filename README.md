# bgeScripts

A collection of scripts used to parse data from main Beyond Good & Evil file container (aka `sally_clean.bf`)

## Script list
- `soundbank.py` - extracts sounds found within binarized sound archives, those are bin files with filename `ff4*.bin`
- `lzoDecompress.py` - decompresses some binarized banks (for example texture banks) and saves uncompressed versions on the hard drive. Requires `python-lzo` to be installed (through package manager of your distro or from pip)
- `univers.py` - parses `univers.ova` file and outputs its contents in CSV format