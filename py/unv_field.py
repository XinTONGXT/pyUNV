

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
from unv_tokenizer import Tokenizer
#
#
#
class Field:
    def __init__(self, type, length, name, description):
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
        
    
    def read(self, tokenizer):
        '''read the value from given buffer, it returns itself so caller can perform
        something like "print field.read().value" '''
        buffer = tokenizer.read(self.length)
        buffer = buffer.strip()
        #TODO: Below check is needed since trying to format an empty string as number gives trouble
        value = None
        if buffer != '':
            value = self.type(buffer)
        else:
            value = self.type() #default value is used based on type
        return value
        
    def write(self, value):
        '''write the given value to a string format and return given value'''
        return self.format_string.format(value)
        
        
#
# Tests
#
import unittest

class TestField(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
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
            
#
if __name__ == '__main__':
    unittest.main()
    