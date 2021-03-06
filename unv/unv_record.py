

__author__ = "Ozgur Yuksel (ozgur@insequor.com)"
__copyright__ = "Copyright (C) 2013 Ozgur Yuksel"
__license__ = "TBD"
__version__ = "0.0"

__doc__ = '''

    TODO: Provide some utility methods to construct records from format strings
    as given in unv descriptions, such as:
        FORMAT(3D25.17)
        #FORMAT(I10,20A1,I10)
                
'''


# Standard

# 3rd Party

# Internal
from common import Storage
from unv_tokenizer import Tokenizer, DataSetIdentifierException
from unv_field import Field

max_line_length = 81

#
#
#
class Record:
    def __init__(self, fields, name=None):
        '''
        @name: (optional) name of the record which can be used by the data set to expose the fields
        if name is not given (None) than all fields are available at data set level, if it is given
        then the values will be part of a record defined by the name and can be accessed as:
        dataSet.<record name>.<field name>
        '''
        self.name = name
        self.fields = fields
        self.field_map = {}
        for field in self.fields:
            self.field_map[field.name] = field

    def defaults(self):
        '''Read all field values and return as an array'''
        values = Storage()
        try:
            for field in self.fields:
                value = field.defaults()
                values[field.name] = value
                try:
                    values[field.name + '_'] = field.describe(value)
                except:
                    pass
        except (StopIteration, DataSetIdentifierException) as e:
            if len(values.keys()) == 0:
                raise e 
            else:
                raise ValueError('Not all records can be read')
        return values
        
    def read(self, tokenizer):
        '''Read all field values and return as an array'''
        values = Storage()
        try:
            for field in self.fields:
                value = field.read(tokenizer)
                values[field.name] = value
                try:
                    values[field.name + '_'] = field.describe(value)
                except:
                    pass
                    
                
        except (StopIteration, DataSetIdentifierException) as e:
            if len(values.keys()) == 0:
                raise e 
            else:
                raise ValueError('Not all records can be read')
            
        return values
        
    def write(self, dict=None, **keyArgs):
        '''Write all field values into buffers and return concatanated buffer
        It will ensure the single row length does not exceed max_line_length
        '''
        paramSet = [{} if dict is None else dict, keyArgs]
        values = {}
        for params in paramSet:
            for key in params:
                values[key] = params[key]
        
        lineLength = 0
        buffer = ''
        for field in self.fields:
            fieldBuffer = field.write(values[field.name])
            fieldLength = len(fieldBuffer)
            if lineLength + fieldLength >= max_line_length:
                lineLength = fieldLength
                if buffer != '':
                    buffer += '\n'
            else:
                lineLength += fieldLength
            buffer += fieldBuffer
        
        #Each record must end with a new line
        if buffer[len(buffer) - 1] != '\n':
            buffer += '\n'

        return buffer
        
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
        self.tokenizer = Tokenizer('         2Foot (pound f)               1\n')
        
    def tearDown(self):
        pass
    
    #Defaults
    def test_defaults_returns_default_values_for_the_fields(self):
        record = Record(self.fields)
        values = record.defaults()
        self.assertEqual(int(), values.units_code)
        
    #Read
    def test_read_ValuesCanBeAccessedByName(self):
        record = Record(self.fields)
        values = record.read(self.tokenizer)
        self.assertEqual(values.units_code, 2)
        self.assertEqual(values.units_description, 'Foot (pound f)')
        self.assertEqual(values.temperature_mode, 1)
    
    def test_read_HandlesNewLineCharactersInTheBuffer(self):
    
        buffer = '''  0.00000000000000000e+00  2.00000000000000000e+00  4.00000000000000000e+00
  6.00000000000000000e+00'''
        fields = []
        for i in range(4):
            fields.append(Field(float, (25, 17), 'value_%i' % i, ''))
        record = Record(fields)
        values = record.read(Tokenizer(buffer))
        for i in range(4):
            self.assertEqual(values['value_%i' % i], i * 2.0)
        
    ##Write
        
    def test_write_AcceptValuesAsNamedParameters(self):
        record = Record(self.fields)
        buffer = record.write(units_code = 2, units_description = 'Foot (pound f)', temperature_mode = 1)
        self.assertEqual(buffer, self.tokenizer.read_all())
        
    def test_write_AcceptValuesAsDictionary(self):
        record = Record(self.fields)
        buffer = record.write({'units_code' : 2, 'units_description' : 'Foot (pound f)', 'temperature_mode' : 1})
        self.assertEqual(buffer, self.tokenizer.read_all())
        
        
    def test_write_HandlesNewLineCharactersInTheBuffer(self):
    
        buffer = '''  0.00000000000000000e+00  2.00000000000000000e+00  4.00000000000000000e+00
  6.00000000000000000e+00\n'''
        fields = []
        values = {}
        for i in range(4):
            fields.append(Field(float, (25, 17), 'value_%i' % i, ''))
            values['value_%i' % i] = i * 2.0
            
        record = Record(fields)
        self.assertEqual(buffer, record.write(values))
    
    def test_writes_two_max_length_strings_in_two_lines(self):
        fields = []
        values = {}
        for i in range(2):
            fields.append(Field(str, 80, 'value_%i' % i, ''))
            values['value_%i' % i] = 'a'
        record = Record(fields)
        buffer = 'a' + ' ' * 79 + '\n' + 'a' + ' ' * 79  + '\n'
        self.assertEqual(buffer, record.write(values))
            
#
if __name__ == '__main__':
    unittest.main()
     
    