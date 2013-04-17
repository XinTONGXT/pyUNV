

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
        
        self.value = None
    
    def read(self, buffer):
        '''read the value from given buffer, it returns itself so caller can perform
        something like "print field.read().value" '''
        if len(buffer) != self.length:
            raise ValueError
        value = self.type(buffer)
        if self.type is str:
            value = value.strip()
        self.value = value
        return self
        
    def write(self, value=None):
        '''write the given value to a string format and return
        given value, if not None is stored as self.value
        it always writes the self.value'''
        if value is not None:
            self.value = value
        return self.format_string.format(self.value)
        
    def parse(self, buffer):
        '''parse the given value, it will use the first part of the buffer to read
           the value and return the remaining part'''
        self.read(buffer[:self.length])
        return buffer[self.length:]
        
        
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
        self.assertEqual(field.read('         5').value, '5')
        
    def test_read_HandlesInt(self):
        field = Field(int, 10, '', '')
        self.assertEqual(field.read('         5').value, 5)
        
    def test_read_HandlesFloat(self):
        field = Field(float, (25, 17), '', '')
        self.assertEqual(field.read('  1.00000000000000000e+01').value, 10.0)
    
    def test_read_RaisesValueErrorIfBufferLengthDoesNotMatch(self):
        field = Field(int, 10, '', '')
        with self.assertRaises(ValueError):
            field.read('       5')
        with self.assertRaises(ValueError):
            field.read('            5')
    
    #Write
    def test_write_ReturnsExpandedString(self):
        field = Field(str, 10, '', '')
        self.assertEqual(field.write('5'), '5         ')
        self.assertEqual(field.write(), '5         ')
    
    def test_write_ReturnsAdjustedStringForInt(self):
        field = Field(int, 10, '', '')
        self.assertEqual(field.write(5), '         5')
        self.assertEqual(field.write(), '         5')
        
    def test_write_ReturnsAdjustedStringForFloat(self):
        field = Field(float, (25, 17), '', '')
        self.assertEqual(field.write(10.0), '  1.00000000000000000e+01')
        self.assertEqual(field.write(), '  1.00000000000000000e+01')
    
    #Parse    
    def test_parse_UpdatesGivenBuffer(self):
        buffer = '    8.000000000000000e-02    2.000000000000000e-02    0.000000000000000e+00'
        field = Field(float, (25, 16), '', '')
        values = [0.08, 0.02, 0.0]
        for val in values:
            buffer = field.parse(buffer)
            self.assertEqual(field.value, val)
            
            
    def test_parse_RaisesValueErrorIfBufferLengthIsShorter(self):
        buffer = '    8.000000000000000e-02    2.000000000000000e-02    0.000000000000e+00'
        field = Field(float, (25, 16), '', '')
        values = [0.08, 0.02]
        for val in values:
            buffer = field.parse(buffer)
            self.assertEqual(field.value, val)
            
        with self.assertRaises(ValueError):
            field.parse(buffer)
    
    def test_parse_UpdatesGivenBufferEvenIfItIsLonger(self):
        buffer = '    8.000000000000000e-02    2.000000000000000e-02    0.000000000000000e+00extrapart'
        field = Field(float, (25, 16), '', '')
        values = [0.08, 0.02, 0.0]
        for val in values:
            buffer = field.parse(buffer)
            self.assertEqual(field.value, val)
        self.assertEqual(buffer, 'extrapart')
          
            
#
if __name__ == '__main__':
    unittest.main()
    