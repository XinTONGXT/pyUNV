

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
              Field(format='1I10', name='units_code', options=UnitsCodeOptions)
            , Field(format='20A1', name='units_desc')
            , Field(format='1I10', name='temperature_mode', options=TemperatureModeOptions)
          ])
        , Record([
              Field(format='1D25.17', name='length')
            , Field(format='1D25.17', name='force')
            , Field(format='1D25.17', name='temperature')
            , Field(format='1D25.17', name='temperature_offset')
          ])
        ]
        
        DataSet.__init__(self, 164, definitionRecords, [], tokenizer)
        self.name = 'Units'
        
    def defaults(self):
        values = DataSet.defaults(self)
        values.units_code = 1
        values.units_desc = self.field_map['units_code'].describe(values.units_code)
        values.temperature_mode = 2
        values.length = 1.0
        values.force = 1.0
        values.temperature = 1.0
        values.temperature_offset = 0.0
        
        return values
#
# Tests
#
import unittest

class TestDataSet164(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    #Defaults
    def test_defaults_returns_the_default_values_for_records(self):
        dataSet = DataSet164(None)
        values = dataSet.defaults()
        self.assertEqual(1, values.units_code)
    
        
#
if __name__ == '__main__':
    unittest.main()
    