

__author__ = "Ozgur Yuksel (ozgur@insequor.com)"
__copyright__ = "Copyright (C) 2013 Ozgur Yuksel"
__license__ = "TBD"
__version__ = "0.0"

__doc__ = '''Some utility methods and options to be shared by other scripts in the package
'''
# Standard

# 3rd Party

# Internal: None, this should not depend on any other
def make_options(buffer, value_type, sep):
    '''Create a dictionary object seperating the buffer first to lines then the using sep
    '''
    options = {}
    lines = buffer.split('\n')
    for line in lines:
        line = line.split(sep)
        if len(line) == 2:
            options[value_type(line[0])] = line[1].strip()
    return options

    
    
 #TODO: Remove the dependency to web.py is the Storage is the only item we use it from there
from web import Storage