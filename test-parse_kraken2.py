# Test parse_kraken2.py
# Run all tests: python test-parse_kraken2.py
# Run one test:  python3 test-parse_kraken2.py TestParserKraken2.test_sort_result_tb
# Run code coverage: coverage run test_applymask.py 
# View code coverage report: coverage report -m
# Generate code coverage html report: coverage html

import unittest
import json

import parse_kraken2

class TestParserKraken2(unittest.TestCase):
    def setUp(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass

    def test_read_kraken2(self):
        input_file = 'data/tb.tab'
        pct_threshold = 1
        num_threshold = 100000
        result = parse_kraken2.read_kraken2(input_file, pct_threshold, num_threshold)
        self.assertTrue('Family' in result.keys())
        self.assertTrue('Genus' in result.keys())
        self.assertTrue('Species complex' in result.keys())
        self.assertTrue('Species' in result.keys())
        self.assertTrue('Mykrobe' in result.keys())
    
    def test_sort_result_tb(self):
        input_file = 'data/tb.tab'
        pct_threshold = 1
        num_threshold = 100000
        result = parse_kraken2.read_kraken2(input_file, pct_threshold, num_threshold)
        sorted_result = parse_kraken2.sort_result(result, pct_threshold, num_threshold)
        self.assertTrue(sorted_result['Family'][0]['name'] == "Mycobacteriaceae")
        self.assertTrue(sorted_result['Genus'][0]['name'] == "Mycobacterium")
        self.assertTrue(sorted_result['Species complex'][0]['name'] == "Mycobacterium tuberculosis complex")
        self.assertTrue(sorted_result['Species'][0]['name'] == "Homo sapiens")
        self.assertTrue(sorted_result['Mykrobe']['report'] == True)
    
    def test_sort_result_abscessus(self):
        input_file = 'data/abscessus.tab'
        pct_threshold = 1
        num_threshold = 100000
        result = parse_kraken2.read_kraken2(input_file, pct_threshold, num_threshold)
        sorted_result = parse_kraken2.sort_result(result, pct_threshold, num_threshold)
        self.assertTrue(sorted_result['Family'][0]['name'] == "Mycobacteriaceae")
        self.assertTrue(sorted_result['Genus'][0]['name'] == "Mycobacteroides")
        self.assertTrue('notes' in sorted_result['Species complex'].keys())
        self.assertTrue(sorted_result['Species'][0]['name'] == "Mycobacteroides abscessus")
        self.assertTrue(sorted_result['Species'][1]['name'] == "Homo sapiens")
        self.assertTrue(sorted_result['Mykrobe']['report'] == True)

    def test_sort_result_mixed(self):
        input_file = 'data/mixed.tab'
        pct_threshold = 1
        num_threshold = 100000
        result = parse_kraken2.read_kraken2(input_file, pct_threshold, num_threshold)
        sorted_result = parse_kraken2.sort_result(result, pct_threshold, num_threshold)
        self.assertTrue(sorted_result['Family'][0]['name'] == "Mycobacteriaceae")
        self.assertTrue(sorted_result['Family'][1]['name'] == "Paenibacillaceae")
        self.assertTrue(sorted_result['Genus'][0]['name'] == "Mycobacterium")
        self.assertTrue(sorted_result['Genus'][1]['name'] == "Paenibacillus")
        self.assertTrue(sorted_result['Species complex'][0]['name'] == "Mycobacterium tuberculosis complex")
        self.assertTrue(sorted_result['Species'][0]['name'] == "Paenibacillus glucanolyticus")
        self.assertTrue(sorted_result['Species'][1]['name'] == "Homo sapiens")
        self.assertTrue(sorted_result['Mykrobe']['report'] == True)

    def test_sort_result_high(self):
        input_file = 'data/high.tab'
        pct_threshold = 1
        num_threshold = 100000
        result = parse_kraken2.read_kraken2(input_file, pct_threshold, num_threshold)
        sorted_result = parse_kraken2.sort_result(result, pct_threshold, num_threshold)
        self.assertTrue(sorted_result['Family'][0]['name'] == "Mycobacteriaceae")
        self.assertTrue(sorted_result['Genus'][0]['name'] == "Mycobacterium")
        self.assertTrue(sorted_result['Species complex'][0]['name'] == "Mycobacterium avium complex (MAC)")
        self.assertTrue(sorted_result['Species'][0]['name'] == "Mycobacterium avium")
        self.assertTrue(sorted_result['Species'][1]['name'] == "Homo sapiens")
        self.assertTrue(sorted_result['Mykrobe']['report'] == True)

    def test_sort_result_low(self):
        input_file = 'data/low.tab'
        pct_threshold = 1
        num_threshold = 100000
        result = parse_kraken2.read_kraken2(input_file, pct_threshold, num_threshold)
        sorted_result = parse_kraken2.sort_result(result, pct_threshold, num_threshold)
        self.assertTrue(sorted_result['Family'][0]['name'] == "Mycobacteriaceae")
        self.assertTrue(sorted_result['Genus'][0]['name'] == "Mycobacterium")
        self.assertTrue(sorted_result['Species complex'][0]['name'] == "Mycobacterium avium complex (MAC)")
        self.assertTrue(sorted_result['Species'][0]['name'] == "Mycobacterium avium")
        self.assertTrue(sorted_result['Species'][1]['name'] == "Homo sapiens")
        self.assertTrue(sorted_result['Mykrobe']['report'] == True)

    def test_sort_result_xenopi(self):
        input_file = 'data/xenopi.tab'
        pct_threshold = 1
        num_threshold = 100000
        result = parse_kraken2.read_kraken2(input_file, pct_threshold, num_threshold)
        sorted_result = parse_kraken2.sort_result(result, pct_threshold, num_threshold)
        self.assertTrue(sorted_result['Family'][0]['name'] == "Mycobacteriaceae")
        self.assertTrue(sorted_result['Genus'][0]['name'] == "Mycobacterium")
        self.assertTrue('notes' in sorted_result['Species complex'].keys())
        self.assertTrue(sorted_result['Species'][0]['name'] == "Homo sapiens")
        self.assertTrue(sorted_result['Mykrobe']['report'] == True)

    def test_sort_result_kansasii(self):
        input_file = 'data/kansasii.tab'
        pct_threshold = 1
        num_threshold = 100000
        result = parse_kraken2.read_kraken2(input_file, pct_threshold, num_threshold)
        sorted_result = parse_kraken2.sort_result(result, pct_threshold, num_threshold)
        self.assertTrue(sorted_result['Family'][0]['name'] == "Bacillaceae")
        self.assertTrue(sorted_result['Family'][1]['name'] == "Mycobacteriaceae")
        self.assertTrue(sorted_result['Genus'][0]['name'] == "Bacillus")
        self.assertTrue(sorted_result['Genus'][1]['name'] == "Mycobacterium")
        self.assertTrue('notes' in sorted_result['Species complex'].keys())
        self.assertTrue(sorted_result['Species'][0]['name'] == "Bacillus paralicheniformis")
        self.assertTrue(sorted_result['Species'][1]['name'] == "Mycobacterium kansasii")
        self.assertTrue(sorted_result['Species'][2]['name'] == "Homo sapiens")
        self.assertTrue(sorted_result['Mykrobe']['report'] == True)

    def test_sort_result_unclassified(self):
        input_file = 'data/unclassified.tab'
        pct_threshold = 1
        num_threshold = 100000
        result = parse_kraken2.read_kraken2(input_file, pct_threshold, num_threshold)
        sorted_result = parse_kraken2.sort_result(result, pct_threshold, num_threshold)

        self.assertTrue('notes' in sorted_result['Family'].keys())
        self.assertTrue('notes' in sorted_result['Genus'].keys())
        self.assertTrue('notes' in sorted_result['Species complex'].keys())
        self.assertTrue('notes' in sorted_result['Species'].keys())
        self.assertTrue(sorted_result['Mykrobe']['report'] == False)
      

if __name__ == "__main__":
    unittest.main()