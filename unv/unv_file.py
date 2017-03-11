

__author__ = "Ozgur Yuksel (ozgur@insequor.com)"
__copyright__ = "Copyright (C) 2013 Ozgur Yuksel"
__license__ = "TBD"
__version__ = "0.0"

__doc__ = '''
'''




# Standard

# 3rd Party

# Internal
from common import data_folder, Stream
from unv_data_set import *
from unv_tokenizer import Tokenizer 

class File:
    '''
    '''
    
    def __get_header(self,):
        return self.headerDataSet.defaults()
        
    header = property(__get_header)
    
    def __get_units(self):
        return self.unitsDataSet.defaults()
        
    units = property(__get_units)
    
    
    def __init__(self, stream):
        '''
        stream: is a read/write (based on new file or not) buffer where the contents will be read
        or writen
        '''
        self.stream = stream
        self.headerDataSet = get_data_set(151, None)
        self.unitsDataSet = get_data_set(164, None)
        self.dataSets = [self.headerDataSet, self.unitsDataSet]
        
    def flush(self):
        '''flush the current content of the file to the given strem
        '''
        formatstring = '{:%i}\n' % (6)
        for dataSet in self.dataSets:
            self.stream.write(data_set_start + '\n')
            self.stream.write(formatstring.format(dataSet.number))
            self.stream.write(dataSet.write())
            self.stream.write(data_set_end + '\n')
        self.dataSet = []
    
    def add(self, dataSet, flush):
        ''' 
        flush: True/False, If True it causes all existing data sets to be flushed to the stream
        '''
        self.dataSets.append(dataSet)
        if flush:
            self.flush()


class ReadFile:
    '''
    '''
    
    def __get_header(self,):
        return self.dataSets[0].values
        
    header = property(__get_header)
    
    def __get_units(self):
        return self.dataSets[1].values
        
    units = property(__get_units)
    
    
    def __init__(self, stream):
        '''
        '''
        assert(stream)
        self.tokenizer = Tokenizer(stream)
        self.dataSets = [dataSet for dataSet in data_sets(self.tokenizer)]
        assert(self.dataSets[0].number == 151)
        assert(self.dataSets[1].number == 164)   

    def data_sets(self, filter):
        '''return the loaded data sets, filtered by data set numbers if filter is given
        '''
        for set in self.dataSets:
            if not filter or set.number in filter:
                yield set      


#
# Tests
#
import unittest

class TestFile(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
        
    #Working with new files - Header
    def test_a_brand_new_file_has_header(self):
        unvFile = File(None)
        self.assertIsNotNone(unvFile.header)
        
    def test_default_header_is_the_defaults_from_record_151(self):
        dataSet151 = get_data_set(151, None)
        refDefaults = dataSet151.defaults()
        
        unvFile = File(None)
        defaults = unvFile.header
        
        for key in refDefaults:
            self.assertEqual(refDefaults[key], defaults[key])
    
    #Working with new files - Units
    def test_a_brand_new_file_has_units(self):
        unvFile = File(None)
        self.assertIsNotNone(unvFile.units)
    
    def test_default_header_is_the_defaults_from_record_164(self):
        dataSet164 = get_data_set(164, None)
        refDefaults = dataSet164.defaults()
        
        unvFile = File(None)
        defaults = unvFile.units
        
        for key in refDefaults:
            self.assertEqual(refDefaults[key], defaults[key])
            
    #Working with new files - Writing
    def test_a_brand_new_file_without_flush_does_not_write_anything(self):
        stream = Stream()
        unvFile = File(stream)
        self.assertEqual('', stream.getvalue())
        
    def test_a_brand_new_file_writes_default_file(self):
        stream = Stream()
        unvFile = File(stream)
        unvFile.flush()
        expectedBuffer = '''    -1
   151
newfile.unv                                                                     
NONE                                                                            
pyUNV                                                                           
                   0         0         0         0
                    
pyUNV                                                                           
02-Jan-14 23:34:49  
    -1
    -1
   164
         1SI: Meter (newton)           2
  1.00000000000000000e+00  1.00000000000000000e+00  1.00000000000000000e+00
  0.00000000000000000e+00
    -1
'''
        #This assertion is not active due to the date time in reference data
        #self.assertEqual(expectedBuffer, stream.getvalue() )
    
        
    
#
if __name__ == '__main__':
    unittest.main()
    