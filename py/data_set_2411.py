

__author__ = "Ozgur Yuksel (ozgur@insequor.com)"
__copyright__ = "Copyright (C) 2013 Ozgur Yuksel"
__license__ = "TBD"
__version__ = "0.0"

__doc__ = ''' '''


# Standard

# 3rd Party

# Internal
from unv_data_set import DataSet, Record, Tokenizer
from unv_field import field, Field

    
#Custom Fields

#
#
class DataSet2411 (DataSet):
    def __init__(self, tokenizer):
        dataRecords = [
              Record([   
                  field('1I10', 'node_label', '')
                , field('1I10', 'export_coordinate_system', '')
                , field('1I10', 'displacement_coordinate_system', '')
                , field('1I10', 'color', '')
              ])
            , Record([field('1P3D25.16', 'coordinate', '')])
        ]
        
        DataSet.__init__(self, 2411, [], dataRecords, tokenizer)
        self.name = 'Nodes - Double Precision'
#
# Tests
#
import unittest

class TestField(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
        
#
if __name__ == '__main__':
    unittest.main()
    