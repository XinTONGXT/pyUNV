

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
import json
# 3rd Party
from web import Storage
# Internal
from unv_tokenizer import Tokenizer, DataSetIdentifierException, dataset_marker

#
#
_types = {
      'A' : str
    , 'D' : float
    , 'E' : float
    , 'I' : int
    , 'X' : str #space field
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
    try:
        r  = int(format[:idx])
    except:
        r = 1
        
    if format[idx] == 'P': #Multi Dimension is requested
        format = format[idx + 1: ]
        idx = 0
        while format[idx].isdigit():
            idx += 1
        d = int(format[:idx])
        
    t = _types[format[idx]]
    if format[idx] == 'X':  #Space character is defined onyl by repeat
        l = 1
        d = 1
    else:
        format = format[idx + 1:]
        if t is float:
            format = format.split('.')
            l = (int(format[0]), int(format[1]) )
        else:
            l = int(format)
        
        if t is str:
            (r, l) = (1, r * l)
    return (r, t, l, d)
    
def field(format, name, description, options=None):
    '''Create new Field objects parsing the format string for dimension, type and length of the field'''
    r, t, l, d = _parse_field_format(format)
    return Field(t, l, name, description, d, options)
    
#
#
class Field:
    def __init__(self 
        , value_type=None
        , length=1
        , name='' 
        , description='' 
        , dimension=1
        , options=None
        , format=None):
        '''
        if @format is given then the @value_type, @length, @dimension is retrieved from it
        '''
        if format is not None:
            r, value_type, length, dimension = _parse_field_format(format)
        
        self.value_type = value_type
        if value_type is float:
            self.length = length[0]
            self.decimals = length[1]
            #Value is written as right alignment in a full length string
            #with the given decimal points and e format
            self.format_string = '{:%i.%ie}' % (self.length, self.decimals)
        else:
            self.length = length
            self.decimals = 0
            #Value is written as right alignment in a full length string
            if value_type is str:
                self.format_string = '{:<%i}' % self.length
            else:
                self.format_string = '{:>%i}' % self.length
        
        self.name = name
        self.description = description  
        self.dimension = dimension
        
        if options != None and type(options) is str:
            newOptions = {}
            lines = options.split('\n')
            for line in lines:
                line = line.split(' - ')
                if len(line) == 2:
                    newOptions[self.value_type(line[0])] = line[1].strip()
            options = newOptions
            
        self.options = options
    
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
                    value = self.value_type(buffer)
                else:
                    value = self.value_type() #default value is used based on type
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
    
    def describe(self, value):
        '''Field object, by default, does not have self.options so this method call
        will raise an exception. Custom fields can provide this dictionary to return
        more descriptive info about a specific value.
        
        For more custom behavior, field classes can override the method completely
        '''
        if value in self.options:
            return self.options[value]
    
    #json
    def __repr__(self):
        s = object.__repr__(self)
        return '<' + 'Field ' + s[1:] + ' ' + str(self.to_json())
       
        
        
        
    def to_json(self):
        value_type = ''
        for k in _types:
            if _types[k] is self.value_type:
                value_type = k
                break
                
        return {
             'value_type': value_type
            , 'length': self.length
            , 'name': self.name
            , 'description': self.description
            , 'dimension': self.dimension
            , 'options': self.options
        }
    
    def from_json(self, dict):
        dict = Storage(dict)
        self.value_type = _types[dict.value_type]
        self.length = dict.length
        self.name = dict.name
        self.description = dict.description
        self.dimension = dict.dimension
        self.options = dict.options
    
class CustomTypeEncoder(json.JSONEncoder):
    '''A custom JSONEncoder class that knows how to encode core custom
    objects.

    Custom objects are encoded as JSON object literals (ie, dicts) with
    one key, '__TypeName__' where 'TypeName' is the actual name of the
    type to which the object belongs.  That single key maps to another
    object literal which is just the __dict__ of the object encoded.'''

    def default(self, obj):
        #if isinstance(obj, Field):
        if hasattr(obj, 'to_json'):
            key = '__%s__' % obj.__class__.__name__
            return { key: obj.to_json() }
        return json.JSONEncoder.default(self, obj)

class CustomTypeDecoder(json.JSONDecoder):
    '''
    '''
    def decode(self, s):
        dict = json.JSONDecoder.decode(self, s)
        if len(dict.keys()) == 1:
            key = dict.keys()[0]
            try:
                #TODO: Perhaps I should make from_json as a class method which will return 
                #the properly initialized object instead of we creating one
                exec 'obj = %s()' % key.strip('_')
                if hasattr(obj, 'from_json'):
                    obj.from_json(dict[key])
                    return obj
            except:
                pass
        return dict
        
#
# Tests
#
import unittest

class TestField(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    #_parse_field_format
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
    
    def test_parse_field_format_SupportsSpace(self):
        self.assertEquals(_parse_field_format('1X'), (1, str, 1, 1))
        
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
        
    #json
    def test_dumps_DumpsTheField(self):
        field = Field(format='1I5', name='test', description='test field')
        dumps = json.dumps(field, cls=CustomTypeEncoder)
        print '\n', dumps
        newField = json.loads(dumps, cls=CustomTypeDecoder)
        print '\n', newField
#
if __name__ == '__main__':
    unittest.main()
    