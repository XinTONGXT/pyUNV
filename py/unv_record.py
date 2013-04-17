

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
from unv_field import Field

max_line_length = 80

#
#
#
class Record:
    def __init__(self, fields):
        '''
        '''
        self.fields = fields
        self.field_map = {}
        for field in self.fields:
            self.field_map[field.name] = field

    def read(self, buffer):
        for field in self.fields:
            buffer = field.parse(buffer)
    
    def write(self, dict=None, **keyArgs):
        '''Write all field values into buffers and return concatanated buffer
        It will ensure the single row length does not exceed max_line_length
        '''
        paramSet = [{} if dict is None else dict, keyArgs]
        
        for params in paramSet:
            for key in params:
                self.field_map[key].value = params[key]
        
        lineLength = 0
        buffer = ''
        for field in self.fields:
            fieldBuffer = field.write()
            fieldLength = len(fieldBuffer)
            if lineLength + fieldLength >= max_line_length:
                lineLength = fieldLength
                buffer += '\n'
            else:
                lineLength += fieldLength
            buffer += fieldBuffer
        return buffer
        
    def __getattr__(self, name):
        '''Handle the access to the values (not the fields) through field names for reading'''
        if name in self.field_map:
            return self.field_map[name].value
        raise AttributeError
        
    def __setattr__(self, name, value):
        '''Handle the access to the values (not the fields) through field names for writing
        Unlike the __getattr__, this method is called for all attribute access so there is a chance
        of recursion here
        '''
        if 'field_map' in self.__dict__:
            field_map = self.__dict__['field_map']
            if name in field_map:
                field_map[name].value = value
        self.__dict__[name] = value
        
        
        
#
# Tests
#
import unittest

class TestRecord(unittest.TestCase):
    def setUp(self):
        #These records are from Record 1 of Data Set 164
        self.fields = [Field(int, 10, 'units_code', 'units code')
                     , Field(str, 20, 'units_description', 'units description')
                     , Field(int, 10, 'temperature_mode', '1 - absolute, 2 - relative')
                    ]
        self.buffer = '         2Foot (pound f)               1'
        
    def tearDown(self):
        pass
    
    #Read
    def test_read_ValuesCanBeAccessedByFieldIndex(self):
        record = Record(self.fields)
        record.read(self.buffer)
        self.assertEqual(record.fields[0].value, 2)
        self.assertEqual(record.fields[1].value, 'Foot (pound f)')
        self.assertEqual(record.fields[2].value, 1)
        
    def test_read_ValuesCanBeAccessedByName(self):
        buffer = '         2Foot (pound f)               1'
        record = Record(self.fields)
        record.read(buffer)
        self.assertEqual(record.units_code, 2)
        self.assertEqual(record.units_description, 'Foot (pound f)')
        self.assertEqual(record.temperature_mode, 1)
    
    def test_read_HandlesNewLineCharactersInTheBuffer(self):
    
        buffer = '''  0.00000000000000000e+00  2.00000000000000000e+00  4.00000000000000000e+00
  6.00000000000000000e+00'''
        fields = []
        for i in range(4):
            fields.append(Field(float, (25, 17), 'value_%i' % i, ''))
        record = Record(fields)
        record.read(buffer)
        self.assertEqual(record.fields[0].value, 0.0)
        self.assertEqual(record.fields[1].value, 2.0)
        self.assertEqual(record.fields[2].value, 4.0)
        self.assertEqual(record.fields[3].value, 6.0)
        
    ##Write
    def test_write_ValuesCanBeAccessedByName(self):
        record = Record(self.fields)
        record.units_code = 2
        self.assertEqual(record.units_code, 2)
        self.assertEqual(record.fields[0].value, record.units_code)
    
    def test_write_ReturnsTheCorrectStringBufferForExistingValues(self):
        record = Record(self.fields)
        record.units_code = 2
        record.units_description = 'Foot (pound f)'
        record.temperature_mode = 1
        buffer = record.write()
        self.assertEqual(buffer, self.buffer)
        
    def test_write_AcceptValuesAsNamedParameters(self):
        record = Record(self.fields)
        buffer = record.write(units_code = 2, units_description = 'Foot (pound f)', temperature_mode = 1)
        self.assertEqual(buffer, self.buffer)
        
    def test_write_AcceptValuesAsDictionary(self):
        record = Record(self.fields)
        buffer = record.write({'units_code' : 2, 'units_description' : 'Foot (pound f)', 'temperature_mode' : 1})
        self.assertEqual(buffer, self.buffer)
        
        
    def test_write_HandlesNewLineCharactersInTheBuffer(self):
    
        buffer = '''  0.00000000000000000e+00  2.00000000000000000e+00  4.00000000000000000e+00
  6.00000000000000000e+00'''
        fields = []
        for i in range(4):
            fields.append(Field(float, (25, 17), 'value_%i' % i, ''))
            fields[i].value = i * 2.0
            
        record = Record(fields)
        self.assertEqual(buffer, record.write())
    
          
            
#
if __name__ == '__main__':
    unittest.main()
    