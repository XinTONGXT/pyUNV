

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

FileTypeOptions = '''0 - Universal
                     1 - Archive
                     2 - Other'''

#
#
class DataSet151 (DataSet):
    def __init__(self, tokenizer):
        definitionRecords = [
          Record([field('80A1', 'model_file_name', '')])
        , Record([field('80A1', 'model_file_description', '')])
        , Record([field('80A1', 'application_created_db', '')])
        , Record([   field('10A1', 'date_db_created', '')
            , field('1I10', 'time_db_created', '')
            , field('1I10', 'db_version', '')
            , field('1I10', 'db_subversion', '')
            , field('1I10', 'file_type', '', FileTypeOptions)
          ])
        , Record([
              field('10A1', 'date_last_saved', '')
            , field('10A1', 'time_last_saved', '')
          ])
        , Record([field('80A1', 'application_created_file', '')])
        , Record([   
              field('10A1', 'date_file_created', '')
            , field('10A1', 'time_file_created', '')
            #Below are in the html but not in the record we have
            #, Field(int,  5, 'release_wrote_file', '')
            #, Field(int,  5, 'version', '')
            #, Field(int,  5, 'host_id', '')
            #, Field(int,  5, 'test_id', '')
            #, Field(int,  5, 'release_counter_per_host', '')
          ])
        ]
        
        DataSet.__init__(self, 151, definitionRecords, [], tokenizer)
        self.name = 'Header'
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
    