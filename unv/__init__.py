

__author__ = "Ozgur Yuksel (ozgur@insequor.com)"
__copyright__ = "Copyright (C) 2013 Ozgur Yuksel"
__license__ = "TBD"
__version__ = "0.0"

__doc__ = '''TODO: Document the script

    
'''
# Standard
import cStringIO

# 3rd Party

# Internal
from unv_tokenizer import Tokenizer
from unv_data_set import * 
from unv_file import ReadFile 

        
    
#
# Tests
# To run all the tests in the folder: python -m unittest discover -p *.py
import unittest

class TestUNV(unittest.TestCase):
    def setUp(self):
        self.buffer = '''    -1
   151
C:\Users\oy\Documents\Projects\bitbucket\UNV\data\UNVScenario.CATAnalysis       
NONE                                                                            
LMS Virtual.Lab Rev 11-SL1                                                      
                                                  
                    
LMS Virtual.Lab Rev 11-SL1                                                      
 17-Apr-13  19:32:03
    -1
    -1
   164
         1 SI - mks (Newton)  2
  1.00000000000000000e+00  1.00000000000000000e+00  1.00000000000000000e+00
  0.00000000000000000e+00
    -1
    -1
  2411
        67         1         1         1
    0.000000000000000e+00    0.000000000000000e+00    0.000000000000000e+00
        68         1         1         1
    0.000000000000000e+00    2.000000000000000e-02    0.000000000000000e+00
        69         1         1         1
    0.000000000000000e+00    4.000000000000000e-02    0.000000000000000e+00
    -1
'''
        self.tokenizer = Tokenizer(self.buffer)
        
    def tearDown(self):
        pass
    
    #get_data_set_number
    def test_get_data_set_number_ReturnsTheDataSetNumber(self):
        tokenizer = Tokenizer('   151\n    -1\n')
        self.assertEqual(get_data_set_number(tokenizer), 151)
        
        
    def test_get_data_set_number_RaisesValueErrorForNegativeNumbers(self):
        with self.assertRaises(ValueError):
            tokenizer = Tokenizer('   -151\n    -1\n')
            get_data_set_number(tokenizer)
            
    def test_get_data_set_number_RaisesValueErrorForNonNumbers(self):
        with self.assertRaises(ValueError):
            tokenizer = Tokenizer('   a151\n    -1\n')
            get_data_set_number(tokenizer)
        
    #data_sets
    def test_data_sets_IteratesThroughAllDataSetNumbers(self):
        dataSets = []
        for dataSet in data_sets(self.tokenizer):
            dataSets.append(dataSet.number)
            dataSet.skip()
        self.assertEqual(dataSets, [151, 164, 2411])
        
    def test_data_sets_CanReadRandomlyTheDefinition(self):
        dataSets = {}
        for dataSet in data_sets(self.tokenizer):
            dataSets[dataSet.number] = dataSet
            #Skip is mandatory at the moment so tokenizer advances to the next data set
            #We should have a way to avoid that
            dataSet.skip()
        unitDataSet = dataSets[164]    
        self.assertEqual(unitDataSet.values.units_code, 1)
        self.assertEqual(unitDataSet.values.units_desc, 'SI - mks (Newton)')
    
    def _test_data_sets_CanReadRandomlyTheData(self):
        self.assertEquals(1, 0, 'Test where we have both definition and data')
        
#
if __name__ == '__main__':
    unittest.main()
        
    