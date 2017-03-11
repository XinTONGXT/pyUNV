

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
from common import Storage
from unv_record import Field, Record
from unv_tokenizer import Tokenizer, DataSetIdentifierException

data_set_start = '    -1'
data_set_end   = '    -1'

#
#
#
def get_data_set(number, tokenizer):
    try:
        exec 'from data_set_%i import DataSet%i' % (number, number)
        exec 'dataSet = DataSet%i (tokenizer)' % number
        return dataSet
    except:
        #print '\n', 'exception: ', number
        return DataSet(number, [], [], tokenizer)
        

#
#
def _num_values(records):
    '''Returns number of values which should be read from the records'''
    return reduce(lambda x, y : len(x.fields) + len(y.fields), records)
    
#
#
def _read_records(records, tokenizer, numValues):
    '''Real all fields from given records and return as a single storage object
    It will raise ValueError if not all fields are read
    '''
    _values = Storage()
    try:
        for record in records:
            values = record.read(tokenizer)
            for key in values:
                _values[key] = values[key]
        return _values
    except (StopIteration, DataSetIdentifierException) as e :
        raise e
        
    raise ValueError('Could not read all the fields')
#
#
#
class DataSet:
    def __init__(self 
        , data_set_number 
        , definition_records=[] 
        , data_records=[] 
        , tokenizer=None
        , name=''):
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
        self.number = data_set_number
        self.definition_records = definition_records
        self.data_records = data_records
        self.tokenizer = tokenizer
        self.name = name
        
        self.field_map = {}
        for record in self.definition_records:
            for field in record.fields:
                self.field_map[field.name] = field
        
        self.__values = None    
        self.__data = None
        if tokenizer:
            self.__startPos = tokenizer.tell()
        else:
            self.__startPos = None
            
    def __getValues(self):
        '''values object keeps all the values from definition records
        We can implement __getattr__ method but this is more explicit. so instead user accessing as
            dataSet.units_code
        it should be accessed as: 
            dataSet.values.units_code
        
        This gives user the ability to loop over all values in a for loop and avoids getattr overloading
        I am not too keen on "values" name could not find one yet
        '''
        if not self.__values:
            self.__values = self.read_definition()
        return self.__values
    values = property(__getValues)
    
    def __getData(self):
        if not self.__data:
            self.__data = self.read_data()
        return self.__data
    data = property(__getData)
    
    def defaults(self):
        '''This method is used to create the default values for the definition records'''
        _values = Storage()
        for record in self.definition_records:
            recordValues = record.defaults()
            if record.name:
                try:
                    values = _values[record.name]
                except:
                    values = Storage()
                    _values[record.name] = values
            else:
                values = _values
            for key in recordValues:
                values[key] = recordValues[key]
        return _values
        
    def read_definition(self):
        _values = Storage()
        
        if not self.tokenizer:
            return self.defaults()
            
        if self.tokenizer.tell() != self.__startPos:
            self.tokenizer.seek(self.__startPos)
            
        for record in self.definition_records:
            recordValues = record.read(self.tokenizer)
            if record.name:
                try:
                    values = _values[record.name]
                except:
                    values = Storage()
                    _values[record.name] = values
            else:
                values = _values
            for key in recordValues:
                values[key] = recordValues[key]
        return _values
        
    def read_data(self):
        _data = []
        try:
            numValues = _num_values(self.data_records)
            while True:
                _data.append(_read_records(self.data_records, self.tokenizer, numValues))
        except (StopIteration, DataSetIdentifierException) as e:
            pass #StopIteration is raised by tokenizer at the end of the stream
        
        return _data
        
    
    def skip(self):
        '''process throught the stream till the end of the dataset
        TODO: perhaps we should keep the tokenizer as the member
        '''
        try:
            while True:
                buffer = self.tokenizer.read_line()
                if buffer == data_set_end:
                    return
                if buffer == '':
                    break
        except (StopIteration):
            pass #StopIteration is raised by tokenizer at the end of the stream
            
        raise ValueError('Data Set Ending identifier is not found')
            
    def write(self):
        buffer = ''
        for record in self.definition_records:
            buffer += record.write(self.values)
        return buffer
        
#
# Tests
#
import unittest

class TestDataSet(unittest.TestCase):
    def setUp(self):
        #FORMAT(I10,20A1,I10)
        #FORMAT(3D25.17)
        
        self.buffer164 = '''         1SI - mks (Newton)            2
  1.00000000000000000e+00  2.00000000000000000e+00  3.00000000000000000e+00
  4.00000000000000000e+00
'''
        
        self.buffer2411 = '''        67         1         1         1
    0.000000000000000e+00    0.000000000000000e+00    0.000000000000000e+00
        68         1         1         1
    0.000000000000000e+00    2.000000000000000e-02    0.000000000000000e+00
        69         1         1         1
    0.000000000000000e+00    4.000000000000000e-02    0.000000000000000e+00
'''
        self.tokenizer2411 = Tokenizer(self.buffer2411)
        
    def tearDown(self):
        pass
    
            
    #Read Definition (values)
    def test_read_FullDataSet(self):
        with Tokenizer(self.buffer164) as tokenizer:
            dataSet = get_data_set(164, tokenizer)
            values = dataSet.read_definition()
            
            self.assertEqual(values.units_code, 1)
            self.assertEqual(values.units_desc, 'SI - mks (Newton)')
            self.assertEqual(values.temperature_mode, 2)
            
            self.assertEqual(values.length, 1.0)
            self.assertEqual(values.force, 2.0)
            self.assertEqual(values.temperature, 3.0)
            self.assertEqual(values.temperature_offset, 4.0)
            
    def test_read_FullDataSetThroughValuesMember(self):
        with Tokenizer(self.buffer164) as tokenizer:
            dataSet = get_data_set(164, tokenizer)
            
            self.assertEqual(dataSet.values.units_code, 1)
            self.assertEqual(dataSet.values.units_desc, 'SI - mks (Newton)')
            self.assertEqual(dataSet.values.temperature_mode, 2)
            
            self.assertEqual(dataSet.values.length, 1.0)
            self.assertEqual(dataSet.values.force, 2.0)
            self.assertEqual(dataSet.values.temperature, 3.0)
            self.assertEqual(dataSet.values.temperature_offset, 4.0)
            
            
    def test_read_FullDataSetThroughNamedRecords(self):
        with Tokenizer(self.buffer164) as tokenizer:
            dataSet = get_data_set(164, tokenizer)
            dataSet.definition_records[0].name = 'units'
            
            self.assertEqual(dataSet.values.units.units_code, 1)
            self.assertEqual(dataSet.values.units.units_desc, 'SI - mks (Newton)')
            self.assertEqual(dataSet.values.units.temperature_mode, 2)
            
            self.assertEqual(dataSet.values.length, 1.0)
            self.assertEqual(dataSet.values.force, 2.0)
            self.assertEqual(dataSet.values.temperature, 3.0)
            self.assertEqual(dataSet.values.temperature_offset, 4.0)
            
            dataSet.definition_records[0].name = None
            
    def test_read_FullDataSetThroughMergedNamedRecords(self):
        with Tokenizer(self.buffer164) as tokenizer:
            dataSet = get_data_set(164, tokenizer)
            dataSet.definition_records[0].name = 'units'
            dataSet.definition_records[1].name = 'units'
            
            self.assertEqual(dataSet.values.units.units_code, 1)
            self.assertEqual(dataSet.values.units.units_desc, 'SI - mks (Newton)')
            self.assertEqual(dataSet.values.units.temperature_mode, 2)
            
            self.assertEqual(dataSet.values.units.length, 1.0)
            self.assertEqual(dataSet.values.units.force, 2.0)
            self.assertEqual(dataSet.values.units.temperature, 3.0)
            self.assertEqual(dataSet.values.units.temperature_offset, 4.0)
            
            dataSet.definition_records[0].name = None
            dataSet.definition_records[1].name = None
            
    #Read Data (data)
    def test_read_data_ReadsTheWholeBuffer(self):
        with Tokenizer(self.buffer2411) as tokenizer:
            dataSet = get_data_set(2411, tokenizer)
            data = dataSet.read_data()
            self.assertEqual(len(data), 3)
            
            for i in range(len(data)):
                self.assertEqual(data[i].node_label, 67 + i)
                self.assertEqual(data[i].coordinate[1], 0.02 * i)

    def test_read_data_ReadsTheBufferUntillDataSetEndIdentifier(self):
        buffer = self.buffer2411 + data_set_end + '\n' + self.buffer2411
        with Tokenizer(buffer) as tokenizer:
            dataSet = get_data_set(2411, tokenizer)
            data = dataSet.read_data()
            self.assertEqual(len(data), 3)
            
            for i in range(len(data)):
                self.assertEqual(data[i].node_label, 67 + i)
                self.assertEqual(data[i].coordinate[1], 0.02 * i)
    
    def test_read_data_RaisesValueErrorIfStreamEndsInTheMiddle(self):
        with Tokenizer(self.buffer2411[:25]) as tokenizer:
            dataSet = get_data_set(2411, tokenizer)
            with self.assertRaises(ValueError):
                dataSet.read_data()
                
    def test_read_data_RaisesValueErrorIfDataSetEndsInTheMiddle(self):
        buffer = self.buffer2411[:25] + data_set_end + '\n' + self.buffer2411[25:] 
        with Tokenizer(buffer) as tokenizer:
            dataSet = get_data_set(2411, tokenizer)
            with self.assertRaises(ValueError):
                dataSet.read_data()
                
                
            
    def test_data_ProvidesAccessToTheReadData(self):
        with Tokenizer(self.buffer2411) as tokenizer:
            dataSet = get_data_set(2411, tokenizer)
            self.assertEqual(len(dataSet.data), 3)
            
            for i in range(len(dataSet.data)):
                self.assertEqual(dataSet.data[i].node_label, 67 + i)
                self.assertEqual(dataSet.data[i].coordinate[1], 0.02 * i)
    
    
    #skip
    def test_skip_GoesTillTheBeginningOfNextDataSet(self):
        buffer = '   asome thjext sdflsk lk; sd;l kasdf\n    -1\nNewText'
        with Tokenizer(buffer) as tokenizer:
            dataSet = DataSet(0, [], [], tokenizer)
            dataSet.skip()
            self.assertEqual(tokenizer.read_line(), 'NewText')
        
    def test_skip_RaisesValueErrorIfEndMarkerIsNotFound(self):
        buffer = '   asome thjext sdflsk lk; sd;l kasdf\n  \n  -1\nNewText'
        with Tokenizer(buffer) as tokenizer:
            dataSet = DataSet(0, [], [], tokenizer)
            with self.assertRaises(ValueError):
                dataSet.skip()
        
    
    
    #Write
    def test_write_FullDataSet(self):
        with Tokenizer(self.buffer164) as tokenizer:
            dataSet = get_data_set(164, tokenizer)
            dataSet.read_definition()
            self.assertEqual(self.buffer164, dataSet.write())
        
        
#
if __name__ == '__main__':
    unittest.main()
    