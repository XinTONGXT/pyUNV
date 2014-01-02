import unittest

from unv_tokenizer import TestTokenizer
from unv_field import  TestField
from unv_record import TestRecord 
from unv_data_set import TestDataSet
from unv_file import TestFile

from data_set_58 import TestDataSet58
from data_set_151 import TestDataSet151
from data_set_164 import TestDataSet164
from data_set_2411 import TestDataSet2411
from data_set_2412 import TestDataSet2412
from data_set_2414 import TestDataSet2414

if __name__ == '__main__':
    print 'running all tests'
    unittest.main()