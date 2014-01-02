

__author__ = "Ozgur Yuksel (ozgur@insequor.com)"
__copyright__ = "Copyright (C) 2013 Ozgur Yuksel"
__license__ = "TBD"
__version__ = "0.0"

__doc__ = ''' '''


# Standard

# 3rd Party

# Internal
from unv_data_set import DataSet, Record, Tokenizer
from unv_field import Field

    
#Custom Fields

#
#
class DataSet2412 (DataSet):
    def __init__(self, tokenizer):
        dataRecords = [
              Record([   
                  Field(format='1I10', name='element_label')
                , Field(format='1I10', name='fe_descriptor_id')
                , Field(format='1I10', name='physical_property_table_number')
                , Field(format='1I10', name='material_property_table_number')
                , Field(format='1I10', name='color')
                , Field(format='1I10', name='number_of_nodes')
              ])
              #TODO: this section from number of nodes on elements and fe_descriptor id
            , Record([Field(format='1P3I10', name='orientation')])
            , Record([Field(format='1P2I10', name='nodes')])
        ]
        
        DataSet.__init__(self, 2412, [], dataRecords, tokenizer)
        self.name = 'Elements'
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
    