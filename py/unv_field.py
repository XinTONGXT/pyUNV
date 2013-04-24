

__author__ = "Ozgur Yuksel (ozgur@insequor.com)"
__copyright__ = "Copyright (C) 2013 Ozgur Yuksel"
__license__ = "TBD"
__version__ = "0.0"

__doc__ = '''
Field Types are Like:
    10A1        10 Alphanumeric Characters
    4I10        4 Integer values written 10 characters each
    3D25.17     3 Double values written 25 characters each with 17 decimals
    1P3D25.16   1 array of 3 doubles, each taking 25 characters each with 17 decimals    
    
    
    TODO: Today for 1P3D25.16 we create 3 Fields, however in the format definition it is 
    one field with 3 values, such as coordinates, You would have one field called coordinates
    and values would be accessed as coordinates[0], [1], [2]. today we have to define 
    coordinate_x, _y, _z. For the completeness it is better to support arrays (dimension) in the 
    field definition
'''


# Standard
from cStringIO import StringIO

# 3rd Party

# Internal
from unv_tokenizer import Tokenizer, DataSetIdentifierException, dataset_marker

#
#
_types = {
      'A' : str
    , 'D' : float
    , 'E' : float
    , 'I' : int
}
    
def _parse_field_format(format):
    '''returns a tuple of values from given format as (repeat, type, length, dimension) where:
        
    TODO: This method perhaps can be written in more elegant way
    '''
    r = 1
    d = 1
    idx = 0
    while format[idx].isdigit():
        idx += 1
    r = int(format[:idx])
    
    if format[idx] == 'P': #Multi Dimension is requested
        format = format[idx + 1: ]
        idx = 0
        while format[idx].isdigit():
            idx += 1
        d = int(format[:idx])
        
    t = _types[format[idx]]
    format = format[idx + 1:]
    if t is float:
        format = format.split('.')
        l = (int(format[0]), int(format[1]) )
    else:
        l = int(format)
    
    if t is str:
        (r, l) = (1, r * l)
    return (r, t, l, d)
    
def field(format, name, description):
    '''Create new Field objects parsing the format string for dimension, type and length of the field'''
    r, t, l, d = _parse_field_format(format)
    return Field(t, l, name, description, d)
    
#
#
class Field:
    def __init__(self, type, length, name, description, dimension=1):
        '''
        Supported Types: 
            A -> str
            I -> int
            D -> float
        '''
        self.type = type
        if type is float:
            self.length = length[0]
            self.decimals = length[1]
            #Value is written as right alignment in a full length string
            #with the given decimal points and e format
            self.format_string = '{:%i.%ie}' % (self.length, self.decimals)
        else:
            self.length = length
            self.decimals = 0
            #Value is written as right alignment in a full length string
            if type is str:
                self.format_string = '{:<%i}' % self.length
            else:
                self.format_string = '{:>%i}' % self.length
        
        self.name = name
        self.description = description  
        self.dimension = dimension
        
    
    def read(self, tokenizer):
        '''read the value from given buffer, it returns itself so caller can perform
        something like "print field.read().value" '''
        readValues = 0
        try:
            values = [None] * self.dimension
            for i in range(self.dimension):
                buffer = tokenizer.read(self.length)
                buffer = buffer.strip()
                #TODO: Below check is needed since trying to format an empty string as number gives trouble
                value = None
                if buffer != '':
                    value = self.type(buffer)
                else:
                    value = self.type() #default value is used based on type
                values[i] = value
                readValues += 1
                
            if self.dimension > 1:
                return values
            else:
                return values[0]
        except (StopIteration, DataSetIdentifierException) as e:
            if readValues > 0 and readValues < self.dimension:
                raise ValueError('Not enough values found to read: ' + str(values))
            else:
                raise e
        
    def write(self, value):
        '''write the given value to a string format and return given value'''
        if self.dimension == 1:
            return self.format_string.format(value)
        else:
            if self.dimension > len(value):
                raise ValueError('Not enough value given to write')
            buffer = ''
            for i in range(self.dimension):
                buffer += self.format_string.format(value[i])
            return buffer
        
        
#
# Tests
#
import unittest

class TestField(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    #make_field
    def test_parse_field_format_SupportsIntegerType(self):
        self.assertEquals(_parse_field_format('1I5'), (1, int, 5, 1))
        self.assertEquals(_parse_field_format('3I7'), (3, int, 7, 1))
    
    def test_parse_field_format_SupportsStrings(self):
        self.assertEquals(_parse_field_format('10A1'), (1, str, 10, 1))
        #TODO: 20A2 might refer to unicode characters which will be handled as normal str at the moment
        self.assertEquals(_parse_field_format('20A2'), (1, str, 40, 1))
        
    def test_parse_field_format_SupportsFloats(self):
        self.assertEquals(_parse_field_format('1E13.5'), (1, float, (13,5), 1))
        self.assertEquals(_parse_field_format('3E13.5'), (3, float, (13,5), 1))
        self.assertEquals(_parse_field_format('1D13.5'), (1, float, (13,5), 1))
        self.assertEquals(_parse_field_format('3D13.5'), (3, float, (13,5), 1))
        
    def test_parse_field_format_SupportsMultiDimensionFloats(self):
        self.assertEquals(_parse_field_format('1P3D13.5'), (1, float, (13,5), 3))
        
        
    #Read
    def test_read_HandlesString(self):
        field = Field(str, 10, '', '')
        with Tokenizer('         5') as tokenizer:
            self.assertEqual(field.read(tokenizer), '5')
        
    def test_read_HandlesInt(self):
        field = Field(int, 10, '', '')
        with Tokenizer('         5') as tokenizer:
            self.assertEqual(field.read(tokenizer), 5)
        
    def test_read_HandlesFloat(self):
        field = Field(float, (25, 17), '', '')
        with Tokenizer('  1.00000000000000000e+01') as tokenizer:
            self.assertEqual(field.read(tokenizer), 10.0)
    
    def test_read_MultiDimensionData(self):
        field = Field(int, 2, '', '', 5)
        with Tokenizer(' 1 3 5 7 9') as tokenizer:
            values = field.read(tokenizer)
            self.assertEqual(len(values), 5)
            for i in range(5):
                self.assertEqual(values[i], i * 2 + 1)
                
    def test_read_RaisesValueErrorIfNotEnoughValueFoundForMultiDimensionData(self):
        field = Field(int, 2, '', '', 7)
        with Tokenizer(' 1 3 5 7 9') as tokenizer:
            with self.assertRaises(ValueError):
                field.read(tokenizer)
    
    def test_read_RaisesValueErrorIfDataSetSeperatorWithinFoundForMultiDimensionData(self):
        field = Field(int, 2, '', '', 7)
        with Tokenizer(' 1 3 5\n' + dataset_marker + '\n 7 9') as tokenizer:
            with self.assertRaises(ValueError):
                field.read(tokenizer)    
            
    #Write
    def test_write_ReturnsExpandedString(self):
        field = Field(str, 10, '', '')
        self.assertEqual(field.write('5'), '5         ')
    
    def test_write_ReturnsAdjustedStringForInt(self):
        field = Field(int, 10, '', '')
        self.assertEqual(field.write(5), '         5')
        
    def test_write_ReturnsAdjustedStringForFloat(self):
        field = Field(float, (25, 17), '', '')
        self.assertEqual(field.write(10.0), '  1.00000000000000000e+01')
            
    def test_write_MultiDimensionData(self):
        field = Field(int, 2, '', '', 5)
        values = [0] * 5
        for i in range(5):
            values[i] = i * 2 + 1
        self.assertEqual(field.write(values), ' 1 3 5 7 9')
        
    def test_write_RaisesValueErrorIfLessValuesAreGivenForMultiDimensionData(self):
        field = Field(int, 2, '', '', 5)
        values = [0] * 3
        with self.assertRaises(ValueError):
            field.write(values)
        
#
if __name__ == '__main__':
    unittest.main()
    