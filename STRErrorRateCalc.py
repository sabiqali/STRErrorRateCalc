#! /usr/bin/env python

import argparse
from tracemalloc import start
import numpy as np
import sys
import csv

class CountCalls:
    def __init__(self, count):
        self.count = count

def load_counts(filename):
    out = dict()
    with open(filename) as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            out[row['read_name']] = CountCalls(row['count'])
    return out

parser = argparse.ArgumentParser()
parser.add_argument('--reference', help='the reference genome', required=False)
parser.add_argument('--counts_file', help='the counts file generated from any of the methods', required=True)
parser.add_argument('--str_file', help='the STR file with all the loci you are looking to analyse', required=True)
parser.add_argument('--config', help='the config file used to get the count', required=True)
args = parser.parse_args()

ref_file = args.reference
counts_file = args.counts_file
loci = args.str_file
config_fh = args.config

data = load_counts(counts_file)

#config_file_header = config_fh.readline()
#loci_header = loci_fh.readline()

#chromosome,begin,end,name,repeat,prefix,suffix = config_fh.readline()

with open(config_fh) as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        chromosome = row['chr']
        begin = row['begin']
        end = row['end']
        name = row['name']
        repeat = row['repeat']
        break

motif_ref_count = 0

with open(loci) as f:
    reader = csv.DictReader(f, delimiter='\t')
    for row in reader:
        motif = row['name'].split('x')[1]
        count = row['name'].split('x')[0]
        if row['chrom'] == chromosome and motif == repeat:
            motif_ref_count = count

print("chromosome\tposition\tmotif\tlocus_name\tref_count\tread_name\tread_count")
for dt in data:
    print(f"{chromosome}\t{start}\t{repeat}\t{name}\t{motif_ref_count}\t{dt}\t{data[dt].count}")

