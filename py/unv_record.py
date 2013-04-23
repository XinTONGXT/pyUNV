

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
from web import Storage

# Internal
from unv_tokenizer import Tokenizer, DataSetIdentifierException
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

    def read(self, tokenizer):
        '''Read all field values and return as an array'''
        values = Storage()
        try:
            for field in self.fields:
                values[field.name] = field.read(tokenizer)
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
                buffer += '\n'
            else:
                lineLength += fieldLength
            buffer += fieldBuffer
        return buffer
    
    if 0: #THESE WILL BE MOVED TO THE DATASET
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
        self.tokenizer = Tokenizer('         2Foot (pound f)               1')
        
    def tearDown(self):
        pass
    
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
  6.00000000000000000e+00'''
        fields = []
        values = {}
        for i in range(4):
            fields.append(Field(float, (25, 17), 'value_%i' % i, ''))
            values['value_%i' % i] = i * 2.0
            
        record = Record(fields)
        self.assertEqual(buffer, record.write(values))
    
          
            
#
if __name__ == '__main__':
    unittest.main()
    