[![Build Status](https://travis-ci.com/oxfordmmm/speciation.svg?branch=master)](https://travis-ci.com/oxfordmmm/speciation)
[![codecov](https://codecov.io/gh/oxfordmmm/speciation/branch/master/graph/badge.svg?token=SZ4T0NHVGM)](https://codecov.io/gh/oxfordmmm/speciation)

# Speciation
Scripts for Mycobacterium Speciation

## Test cases

|Test Samples |Family                                              |Genus                                           | Species complex                                                                | Species                                                              | Mykrobe |
|-------------|----------------------------------------------------|------------------------------------------------|--------------------------------------------------------------------------------|----------------------------------------------------------------------|---------|
|tb           |Mycobacteriaceae                                    |Mycobacterium                                   | Mycobacterium tuberculosis complex                                             | Mycobacterium tuberculosis, Homo sapiens                             | True    |
|high(avium)  |Mycobacteriaceae                                    |Mycobacterium                                   | Mycobacterium avium complex (MAC), Mycobacterium tuberculosis complex          | Mycobacterium avium, Homo sapiens                                    | True    |
|low (avium)  |Mycobacteriaceae                                    |Mycobacterium                                   | Mycobacterium avium complex (MAC), Mycobacterium tuberculosis complex          | Mycobacterium avium, Mycobacterium tuberculosis,Homo sapiens         | True    |
|mixed        |Mycobacteriaceae,Paenibacillaceae                   |Mycobacterium, Paenibacillus                    | Mycobacterium tuberculosis complex                                             | Paenibacillus glucanolyticus, Mycobacterium tuberculosis,Homo sapiens| True    |
|abscessus    |Mycobacteriaceae                                    |Mycobacteroides                                 | N/A                                                                            | Mycobacteroides abscessus, Homo sapiens                              | True    |
|xenopi       |Mycobacteriaceae, Streptococcaceae, Nocardiaceae    |Mycobacterium, Nocardiaceae, Mycolicibacterium  | N/A                                                                            | Homo sapiens                                                         | True    |
|kansasii     |Bacillaceae,Mycobacteriaceae                        |Bacillus, Mycobacterium                         | N/A                                                                            | Bacillus paralicheniformis, Mycobacterium kansasii, Homo sapiens     | False   |
|unclassified |N/A                                                 |N/A                                             | N/A                                                                            | N/A                                                                  | False   |
