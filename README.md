[![Build Status](https://travis-ci.com/oxfordmmm/speciation.svg?branch=master)](https://travis-ci.com/oxfordmmm/speciation)
[![codecov](https://codecov.io/gh/oxfordmmm/speciation/branch/master/graph/badge.svg?token=SZ4T0NHVGM)](https://codecov.io/gh/oxfordmmm/speciation)

# Mycobacterial Speciation

The first step of SP3's "speciation" module is made by Kraken2, which classifies reads according to their most likely taxonomic clade.
The Kraken2 output is parsed in order to:

  1. report the composition of the sample in terms of family, genus, and species, counting only those classifications represented by a minimum of 10,000 reads, and > 1% of the total reads. 'Species complex' classifications (in Kraken's terminology, the 'G1' clade) are also reported if the top family hit is Mycobacteriaceae. Human reads are always reported, regardless of minimum thresholds.
  2.  detect potential contaminants, warning the user if the sample does not appear to be a single bacterial isolate.
  3.  flag the sample for further classification using Mykrobe (the second step of the SP3 "speciation" module), should the sample appear to be mycobacterial, or a mixture containing M. tuberculosis reads.
  4.  fail the sample - stop further SP3 processing - should minimum quality requirements not be met.

## Warnings

SP3's Kraken-report parser will warn the user if the sample:
1. has no species (S), species complex (G1), genus (G), or family (F) classifications represented by > 10,000 reads AND > 1% of the total reads.
2. has a top family hit of Mycobacteriaceae but a top genus or species hit whose name is other than Mycobact*.
3. contains multiple S-level classifications meeting the above thresholds, not including human (this is a sign the sample contains a contaminating species).
4. contains multiple G1-level classifications meeting the above thresholds (this is a sign the sample is mixed-mycobacterial).

## Test cases
We used following test cases. 
1. tb - Sample is a single isolate of M. tuberculosis.
* Warnings raised: none.
* Failure at Kraken: no.
* Call Mykrobe: yes.

2. high (avium) - Sample is a mixture of reads with different G1 classifications: both M. avium (c. 90%) and M. tuberculosis (c. 2%) complexes.
* Warnings raised: sample is mixed-mycobacterial.
* Failure at Kraken: no.
* Call Mykrobe: yes.

3. low (avium) - Sample is a mixture of reads with different S classifications: both M. avium (c. 20%) and M. tuberculosis (c. 8%).
* Warnings raised: sample is mixed-mycobacterial; sample contains reads from multiple species.
* Failure at Kraken: no.
* Call Mykrobe: yes.

4. mixed - Sample is M. tuberculosis contaminated with c. 30% Paenibacillus glucanolyticus.
* Warnings raised: sample contains reads from multiple species; top family classification is mycobacterial but this is not consistent with top genus or species classifications.
* Failure at Kraken: no.
* Call Mykrobe: yes.

5. abscessus - Sample is a single isolate of Mycobacteroides abscessus.
* Warnings raised: no species complex classifications meet thresholds of > 10,000 reads and > 1% of total reads (note that this warning can be ignored: there is no associated G1 clade for Mycobacteroides abscessus).
* Failure at Kraken: no.
* Call Mykrobe: yes.

6. xenopi - Sample is a mixture of reads from 2 mycobacterial species complexes (M. avium and M. simiae), contaminated with Streptococcus gordonii.
* Warnings raised: sample is mixed-mycobacterial; sample contains reads from multiple species; top family classification is mycobacterial but this is not consistent with top genus or species classifications.
* Failure at Kraken: no.
* Call Mykrobe: yes.

7. kansasii - Sample is non-tuberculosis mycobacteria (M. kansasii) contaminated with c. 70% Bacillus paralicheniformis.
* Warnings raised: sample contains reads from multiple species.
* Failure at Kraken: yes.
* Call Mykrobe: no.

8. unclassified - Sample is a single isolate of M. tuberculosis, but with very few reads (< 5k)
* Warnings raised: no family, species, or genus classifications meet thresholds of > 10,000 reads and 1% of total reads.
* Failure at Kraken: yes.
* Call Mykrobe: no.

## Test result

|Test Samples |Family                                              |Genus                                           | Species complex                                                                | Species                                                              | Mykrobe | Mixed or contaminated| Multiple mycobacterial| Family <> Genus/Species|  Sample     |          
|-------------|----------------------------------------------------|------------------------------------------------|--------------------------------------------------------------------------------|----------------------------------------------------------------------|---------|----------------------|-----------------------|------------------------|-------------|
|tb           |Mycobacteriaceae                                    |Mycobacterium                                   | Mycobacterium tuberculosis complex                                             | Mycobacterium tuberculosis, Homo sapiens                             | True    |                      |                       |                        | tb          |
|high(avium)  |Mycobacteriaceae                                    |Mycobacterium                                   | Mycobacterium avium complex (MAC), Mycobacterium tuberculosis complex          | Mycobacterium avium, Homo sapiens                                    | True    |                      | True                  |                        | high(avium) |
|low (avium)  |Mycobacteriaceae                                    |Mycobacterium                                   | Mycobacterium avium complex (MAC), Mycobacterium tuberculosis complex          | Mycobacterium avium, Mycobacterium tuberculosis,Homo sapiens         | True    | True                 | True                  |                        | low(avium)  |
|mixed        |Mycobacteriaceae,Paenibacillaceae                   |Mycobacterium, Paenibacillus                    | Mycobacterium tuberculosis complex                                             | Paenibacillus glucanolyticus, Mycobacterium tuberculosis,Homo sapiens| True    | True                 |                       | True                   | mixed       |
|abscessus    |Mycobacteriaceae                                    |Mycobacteroides                                 | N/A                                                                            | Mycobacteroides abscessus, Homo sapiens                              | True    |                      |                       |                        | abscessus   |
|xenopi       |Mycobacteriaceae, Streptococcaceae, Nocardiaceae    |Mycobacterium, Nocardiaceae, Mycolicibacterium  | Mycobacterium avium complex (MAC), Mycobacterium simiae complex                | Streptococcus gordonii, Mycobacterium avium, Homo sapiens            | True    | True                 | True                  | True                   | xenopi      |
|kansasii     |Bacillaceae,Mycobacteriaceae                        |Bacillus, Mycobacterium                         | N/A                                                                            | Bacillus paralicheniformis, Mycobacterium kansasii, Homo sapiens     | False   | True                 |                       |                        | kansasii    |
|unclassified |N/A                                                 |N/A                                             | N/A                                                                            | N/A                                                                  | False   |                      |                       |                        | unclassified|   

## Run Python Parser
#### Get code
```
git clone https://github.com/oxfordmmm/speciation

```
#### Run Parser
```
python3 parse_kraken2.py -k data/abscessus.tab -o abscessus.json
```
#### Run Tests
```
python3 test-parse_kraken2.py
```
#### Update all outputs
```
sh update.sh
```
