# Test parse_mykrobe.py
# Run all tests: python test-parse_mykrobe.py
# Run one test:  python3 test-parse_mykrobe.py TestParserMykrobe.test_mykrobe1
#

import unittest
import json

import parse_mykrobe

def read_file(input):
    with open(input) as mykrobe:
        return json.load(mykrobe)

class TestParserMykrobe(unittest.TestCase):
    def setUp(self):
        pass
    
    @classmethod
    def tearDownClass(cls):
        pass

    def test_result(self):
        input_file = 'data/mykrobe1.json'
        input_data = read_file(input_file)
        
        result = parse_mykrobe.report_species(input_data)
        self.assertTrue('phylo_group' in result.keys())
        self.assertTrue('sub_complex' in result.keys())
        self.assertTrue('species' in result.keys())
        self.assertTrue('lineages' in result.keys())

    def test_mykrobe1(self):
        input_file = 'data/mykrobe1.json'
        input_data = read_file(input_file)
       
        result = parse_mykrobe.report_species(input_data)
        result_lineages = result['lineages']
        self.assertTrue('lineage3' in result_lineages.keys())
        result_mutations = result_lineages['lineage3']
        self.assertTrue('C3273107A' in result_mutations.keys())

    def test_mykrobe2(self):
        input_file = 'data/mykrobe2.json'
        input_data = read_file(input_file)
       
        result = parse_mykrobe.report_species(input_data)
        result_lineages = result['lineages']

        self.assertTrue('lineage1' in result_lineages.keys())
        result_mutations1 = result_lineages['lineage1']
        self.assertTrue('G615938A' in result_mutations1.keys())

        self.assertTrue('lineage1.1' in result_lineages.keys())
        result_mutations2 = result_lineages['lineage1.1']
        self.assertTrue('G4404247A' in result_mutations2.keys())

        self.assertTrue('lineage1.1.2' in result_lineages.keys())
        result_mutations3 = result_lineages['lineage1.1.2']
        self.assertTrue('G2622402A' in result_mutations3.keys())

    def test_mykrobe3(self):
        input_file = 'data/mykrobe3.json'
        input_data = read_file(input_file)
       
        result = parse_mykrobe.report_species(input_data)
        result_lineages = result['lineages']

        self.assertTrue('lineage2' in result_lineages.keys())
        result_mutations1 = result_lineages['lineage2']
        self.assertTrue('G497491A' in result_mutations1.keys())

        self.assertTrue('lineage2.2' in result_lineages.keys())
        result_mutations2 = result_lineages['lineage2.2']
        self.assertTrue('G2505085A' in result_mutations2.keys())

        self.assertTrue('lineage2.2.5' in result_lineages.keys())
        result_mutations3 = result_lineages['lineage2.2.5']
        self.assertTrue('G1059643A' in result_mutations3.keys())

if __name__ == "__main__":
    unittest.main()
