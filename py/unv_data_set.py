

__author__ = "Ozgur Yuksel (ozgur@insequor.com)"
__copyright__ = "Copyright (C) 2013 Ozgur Yuksel"
__license__ = "TBD"
__version__ = "0.0"

__doc__ = '''
Sample Record 164:
Record 1:       FORMAT(I10,20A1,I10)
                Field 1      -- units code
                                = 1 - SI: Meter (newton)
                                = 2 - BG: Foot (pound f)
                                = 3 - MG: Meter (kilogram f)
                                = 4 - BA: Foot (poundal)
                                = 5 - MM: mm (milli newton)
                                = 6 - CM: cm (centi newton)
                                = 7 - IN: Inch (pound f)
                                = 8 - GM: mm (kilogram f)
                                = 9 - US: USER_DEFINED
                                = 10- MN: mm (newton)
                Field 2      -- units description (used for
                                documentation only)
                Field 3      -- temperature mode
                                = 1 - absolute
                                = 2 - relative
Record 2:       FORMAT(3D25.17)
                Unit factors for converting universal file units to SI.
                To convert from universal file units to SI divide by
                the appropriate factor listed below.
                Field 1      -- length
                Field 2      -- force
                Field 3      -- temperature
                Field 4      -- temperature offset
    -1
   164
         1 SI - mks (Newton)  2
  1.00000000000000000e+00  1.00000000000000000e+00  1.00000000000000000e+00
  0.00000000000000000e+00
    -1
                
'''


# Standard

# 3rd Party

# Internal
from unv_record import Field, Record

#
#
#
class DataSet:
    def __init__(self, data_set_number, definition_records, data_records):
        '''A Data Set has a unique number and a set of records. 
        There are two types of records: 
        - Definition Records: They appear ones in the data aet
        - Data Records: They can appear multiple times in the data set, they come
        after the definition records
        
        Both groups are optional, which means a data set might contain only definition
        or only description records, as well as having both of them. Althought technically 
        possible, in practice you wouldn't have a data set without any record
        
        A data set buffer lies between the data set number and the data set end identifier
        (both excluded)
        '''
        self.data_set_number = data_set_number
        self.definition_records = definition_records
        self.data_records = data_records
    
    def read(self, buffer):
        '''
        TODO: End of line characters in the buffer creates trouble while traversing throught
        the buffer. Moving through the buffer should consider the EOL and ignore them, however
        it is not implemented tet. When we search for the buffer for the field (Field.parse) we 
        should get till the field length or EOL, whichever comes first
        
        Below line will create trouble if buffer contains comment lines (which looks like possible
        according to the documentation)
        '''
        buffer = buffer.replace('\n', '')
        
        for record in self.definition_records:
            buffer = record.parse(buffer)
        return self
        
    def write(self):
        buffer = ''
        for record in self.definition_records:
            buffer += record.write() + '\n'
            
        return buffer
        
#
# Tests
#
import unittest

class TestDataSet(unittest.TestCase):
    def setUp(self):
        #FORMAT(I10,20A1,I10)
        #FORMAT(3D25.17)
        self.definitionRecords = [
              Record([Field(int, 10, '', ''), Field(str, 20, '', ''), Field(int, 10, '', '')])
            , Record([Field(float, (25, 17), '', '')
                    , Field(float, (25, 17), '', '') 
                    , Field(float, (25, 17), '', '')
                    , Field(float, (25, 17), '', '')])
        ]
        self.buffer = '''         1SI - mks (Newton)            2
  1.00000000000000000e+00  2.00000000000000000e+00  3.00000000000000000e+00
  4.00000000000000000e+00
'''
        
        
    def tearDown(self):
        pass
    
    def test_read_FullDataSet(self):
        dataSet = DataSet(164, self.definitionRecords, [])
        dataSet.read(self.buffer)
        self.assertEqual(dataSet.definition_records[0].fields[0].value, 1)
        self.assertEqual(dataSet.definition_records[0].fields[1].value, 'SI - mks (Newton)')
        self.assertEqual(dataSet.definition_records[0].fields[2].value, 2)
        
        self.assertEqual(dataSet.definition_records[1].fields[0].value, 1.0)
        self.assertEqual(dataSet.definition_records[1].fields[1].value, 2.0)
        self.assertEqual(dataSet.definition_records[1].fields[2].value, 3.0)
        self.assertEqual(dataSet.definition_records[1].fields[3].value, 4.0)
    
    def test_write_FullDataSet(self):
        dataSet = DataSet(164, self.definitionRecords, [])
        dataSet.read(self.buffer)
        self.assertEqual(dataSet.write(), self.buffer)
        
        
#
if __name__ == '__main__':
    unittest.main()
    