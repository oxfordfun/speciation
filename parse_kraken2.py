#!/usr/bin/env python3
# Kraken2 output explained: https://github.com/DerrickWood/kraken2/wiki/Manual#output-formats. 

import sys
import json
import argparse
from collections import defaultdict

def read_kraken2(file_name, pct_threshold, num_threshold):
    with open(file_name) as kraken2:
        lines = kraken2.readlines()
    
    result = defaultdict(list)
    result['Thresholds'] = {'percentage': pct_threshold, 'reads': num_threshold}
    result['Mykrobe'] = {'report': False, 'notes': ''}
    
    for  line in lines:
        pc_frags, frags_rooted, _, rank_code, ncbi_taxon_id, name = line.split('\t')
        pc_frags = pc_frags.strip()
        name = name.replace('\n','').strip()
        pc_frags_num = float(pc_frags)
        frags_rooted_num = int(frags_rooted)
        ncbi_taxon_id = int(ncbi_taxon_id)

        if (pc_frags_num  >= pct_threshold  and frags_rooted_num >= num_threshold) or  name == 'Homo sapiens':
            if 	rank_code == 'S':
                result['Species'].append({'reads': frags_rooted_num, 'percentage': pc_frags_num, 'name': name, 'taxon': ncbi_taxon_id})
            if  rank_code == 'G':
                result['Genus'].append({'reads': frags_rooted_num, 'percentage': pc_frags_num, 'name': name, 'taxon': ncbi_taxon_id})
            if  rank_code == 'F':
                result['Family'].append({'reads': frags_rooted_num, 'percentage': pc_frags_num, 'name': name, 'taxon': ncbi_taxon_id})
            if  ('Mycobact' in name) and (rank_code == 'G1'):
                result['Species complex'].append({'reads': frags_rooted_num, 'percentage': pc_frags_num, 'name': name, 'taxon': ncbi_taxon_id})
    return result

def sort_result(result, pct_threshold, num_threshold):
    if len(result['Family']) == 0: 
         result['Family'] = {
            "notes": f'No family classification meets thresholds of > {num_threshold} reads and > {pct_threshold} % of total reads.'
            }
    else:
        result['Family'] = sorted(result['Family'], key=lambda k: k['reads'], reverse=True)
        if  (result['Family'][0]['name'] == 'Mycobacteriaceae'):
                    result['Mykrobe']['report']= True

    if len(result['Species']) == 0: 
        result['Species'] = {
            "notes": f'No species classification meets thresholds of > {num_threshold} reads and > {pct_threshold} % of total reads.'
            }
    else:
        result['Species'] = sorted(result['Species'], key=lambda k: k['reads'], reverse=True)

    if len(result['Genus']) == 0:
        result['Genus'] = {
            "notes": f'No genus classification meets thresholds of > {num_threshold} reads and > {pct_threshold} % of total reads'
            }
    else:
        result['Genus'] = sorted(result['Genus'], key=lambda k: k['reads'], reverse=True)

    if len(result['Species complex']) == 0:
        result['Species complex'] = {           
            "notes": f'No Mycobacterium tuberculosis complex meets thresholds of > {num_threshold} reads and > {pct_threshold} % of total reads'
            }
    else:
        result['Species complex'] = sorted(result['Species complex'], key=lambda k: k['reads'], reverse=True)
        if result['Species complex'][0]['name'] == 'Mycobacterium tuberculosis complex':
            result['Mykrobe']['notes'] = 'For higher-resolution classification, see Mykrobe report.'
        else:
            result['Mykrobe']['notes'] = 'Sample is mixed or contaminated. Be cautious with further processing.'       

    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--kraken_file", help="kraken2 output file")
    parser.add_argument("-p", "--pct_reads", default=1, help="threshold of percentage of reads, default 1%")
    parser.add_argument("-n", "--number_reads", default=10000, help="threshold of number of reads, default 10k")
    parser.add_argument("-o", "--output_file", default='output.json', help="output json file, default output.json")
    args = parser.parse_args()

    print(f'File:{args.kraken_file}, pct_reads: {args.pct_reads}, number_reads: {args.number_reads}')
    result = read_kraken2(args.kraken_file, args.pct_reads, args.number_reads)
    output = sort_result(result, args.pct_reads, args.number_reads)
    pretty_output = json.dumps(output, indent=4)
    print(pretty_output)

    with open(args.output_file, 'w') as outfile:
        outfile.write(pretty_output)
