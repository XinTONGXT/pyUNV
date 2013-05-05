

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
UnitsCodeOptions = '''1 - SI: Meter (newton)
                      2 - BG: Foot (pound f)
                      3 - MG: Meter (kilogram f)
                      4 - BA: Foot (poundal)
                      5 - MM: mm (milli newton)
                      6 - CM: cm (centi newton)
                      7 - IN: Inch (pound f)
                      8 - GM: mm (kilogram f)
                      9 - US: USER_DEFINED
                      10- MN: mm (newton)'''

TemperatureModeOptions = '''1 - absolute
                            2 - relative'''                      
#
#
class DataSet164 (DataSet):
    def __init__(self, tokenizer):
        definitionRecords = [
          Record([   
              field('1I10', 'units_code', '', UnitsCodeOptions)
            , field('20A1', 'units_desc', '')
            , field('1I10', 'temperature_mode', '', TemperatureModeOptions)
          ])
        , Record([
              field('1D25.17', 'length', '')
            , field('1D25.17', 'force', '')
            , field('1D25.17', 'temperature', '')
            , field('1D25.17', 'temperature_offset', '')
          ])
        ]
        
        DataSet.__init__(self, 164, definitionRecords, [], tokenizer)
        self.name = 'Units'
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
    