

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

FileTypeOptions = '''0 - Universal
                     1 - Archive
                     2 - Other'''

#
#
class DataSet151 (DataSet):
    def __init__(self, tokenizer):
        definitionRecords = [
          Record([Field(format='80A1', name='model_file_name')])
        , Record([Field(format='80A1', name='model_file_description')])
        , Record([Field(format='80A1', name='application_created_db')])
        , Record([
              Field(format='10A1', name='date_db_created')
            , Field(format='1I10', name='time_db_created')
            , Field(format='1I10', name='db_version')
            , Field(format='1I10', name='db_subversion')
            , Field(format='1I10', name='file_type', options=FileTypeOptions)
          ])
        , Record([
              Field(format='10A1', name='date_last_saved')
            , Field(format='10A1', name='time_last_saved')
          ])
        , Record([Field(format='80A1', name='application_created_file')])
        , Record([   
              Field(format='10A1', name='date_file_created')
            , Field(format='10A1', name='time_file_created')
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

class TestDataSet151(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
        
#
if __name__ == '__main__':
    unittest.main()
    