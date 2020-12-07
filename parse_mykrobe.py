#!/usr/bin/env python3
# Mykrobe explained: https://github.com/Mykrobe-tools/mykrobe

import sys
import json
import argparse
from collections import defaultdict

def report_species(mykrobe_data):
    data = mykrobe_data['tb_sample_id']['phylogenetics']
    result = defaultdict(dict)
    result['phylo_group'] = data['phylo_group']
    result['sub_complex'] = data['sub_complex']
    result['species'] = data['species']
    lineages = data['lineage']['lineage']
    r_lineages = dict()
    for lineage in lineages:
        l_calls = data['lineage']['calls'][lineage]
        for k, v in l_calls.items():
            mutations = dict()
            for mut,mut_info in v.items():
                coverage = mut_info['info']['coverage']['alternate']
                mutations[mut] = coverage
            r_lineages[k] = mutations
    result['lineages'] = r_lineages
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-m", "--mykrobe_file", help="mykrobe output file")
    args = parser.parse_args()
    with open(args.mykrobe_file) as mykrobe:
        data = json.load(mykrobe)
    pretty_output = json.dumps(report_species(data), indent=4)
    print(pretty_output)
