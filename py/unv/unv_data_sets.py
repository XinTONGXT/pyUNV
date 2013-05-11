

__author__ = "Ozgur Yuksel (ozgur@insequor.com)"
__copyright__ = "Copyright (C) 2013 Ozgur Yuksel"
__license__ = "TBD"
__version__ = "0.0"

__doc__ = '''TODO: Document the script'''
# Standard
import cStringIO

# 3rd Party

# Internal
from unv_field import field
from unv_record import Record



if __name__ == '__main__':
    print 'unv_data_sets.py'
    number = 151
    exec 'from data_set_%i import DataSet%i' % (number, number)
    exec 'dataSet = DataSet%i (None) ' % number
    print dataSet