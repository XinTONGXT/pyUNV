

__author__ = "Ozgur Yuksel (ozgur@insequor.com)"
__copyright__ = "Copyright (C) 2013 Ozgur Yuksel"
__license__ = "TBD"
__version__ = "0.0"

__doc__ = '''
'''




# Standard
from cStringIO import StringIO


# 3rd Party

# Internal

data_folder = '../../data/'
dataset_marker  = '    -1'

class DataSetIdentifierException(Exception):
    pass
    
#
# Some Utility Methods
#
#We can't subclass StringIO since it is a method, so we wrap it
class Tokenizer:
    '''
    TODO:
        self,line and DataSetIdentifierException are not tested here but in other places
        It would be still nice to test it here
    '''
    def __init__(self, buffer):
        if hasattr(buffer, 'readline'):
            self.stream = buffer
        else:
            self.stream = StringIO(buffer)
        self.line = ''
        
    def read(self, length):
        if self.line == '':
            self.line = self.stream.readline(-1)
            if self.line == dataset_marker or self.line[:-1] == dataset_marker:
                raise DataSetIdentifierException
        
        buffer = self.line[:length]
        self.line = self.line[length:]
        
        if buffer == '':
            raise StopIteration('Empty string is returned from stream')
            
        if buffer == '\n':
            return self.read(length)
        if buffer.endswith('\n'):
            buffer = buffer[:-1]
        return buffer
    
    def read_line(self):
        self.line = ''
        buffer = self.stream.readline(-1)
        if buffer.endswith('\n'):
            buffer = buffer[:-1]
        return buffer
        
    def read_all(self):
        self.line = ''
        return self.stream.read()
    
    def tell(self):
        return self.stream.tell() - len(self.line)
        
    def seek(self, pos):
        return self.stream.seek(pos)
        
    def close(self):
        self.stream.close()
        
    #__enter__ and __exit__ are required to be used with "with" statements
    def __enter__(self):
        return self
        
    def __exit__(self, type, value, traceback):
        self.close()



#
# Tests
#
import unittest

class TestField(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
    #Tokenizer with String Buffers
    def test_read_ReturnsSameLengthAsItIsAsked(self):
        tokenizer = Tokenizer('123456789')
        self.assertEqual(tokenizer.read(5), '12345')
        self.assertEqual(tokenizer.read(4), '6789')
        
    def test_read_ReturnsTillEOLIfItIsBeforeTheLengthAsked(self):
        with Tokenizer('12\n3456789') as tokenizer:
            self.assertEqual(tokenizer.read(5), '12')
            self.assertEqual(tokenizer.read(12), '3456789')
            
    def test_read_RaisesStopIterationIfEOFReached(self):
        with Tokenizer('12\n3456789') as tokenizer:
            self.assertEqual(tokenizer.read(5), '12')
            self.assertEqual(tokenizer.read(12), '3456789')
            with self.assertRaises(StopIteration):
                tokenizer.read(2)
    
    def test_read_SuppressesTheEOLJustAtTheBeginningOfTheBuffer(self):
        with Tokenizer('12\n3456789') as tokenizer:
            self.assertEqual(tokenizer.read(2), '12')
            self.assertEqual(tokenizer.read(7), '3456789')

    def test_tell_ReturnsTheCurrentPosition(self):
        tokenizer = Tokenizer('1234567890123456789')
        self.assertEqual(tokenizer.tell(), 0)
        tokenizer.read(5)
        self.assertEqual(tokenizer.tell(), 5)
        
    def test_seek_SetsTheCurrentPosition(self):
        tokenizer = Tokenizer('12345678901234567890')
        tokenizer.seek(5)
        self.assertEqual(tokenizer.read(7), '6789012')
        
    #Tokenizer with File Buffers
    def test_read_FileReturnsSameLengthAsItIsAsked(self):
        tokenizer = Tokenizer(open(data_folder + '/tokenizer.txt', 'r'))
        self.assertEqual(tokenizer.read(5), '12345')
        self.assertEqual(tokenizer.read(4), '6789')
    
    def test_seek_FileSetsTheCurrentPosition(self):
        tokenizer = Tokenizer(open(data_folder + 'tokenizer.txt', 'r'))
        tokenizer.seek(5)
        self.assertEqual(tokenizer.read(7), '6789012')
        
#
if __name__ == '__main__':
    unittest.main()
    