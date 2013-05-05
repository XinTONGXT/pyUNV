

__author__ = "Ozgur Yuksel (ozgur@insequor.com)"
__copyright__ = "Copyright (C) 2013 Ozgur Yuksel"
__license__ = "TBD"
__version__ = "0.0"

__doc__ = ''' '''


# Standard

# 3rd Party

# Internal
from unv_data_set import DataSet, Record, Tokenizer
from unv_field import field, Field

    
#Custom Fields

#
#TODO: WORK IN PROCESS
class DataSet2414 (DataSet):
    def __init__(self, tokenizer):
        definitionRecords = [
              Record([field('1I10', 'label', '')])
            , Record([field('40A2', 'name', '')])
            , Record([field('1I10', 'location', '')])
            , Record([field('40A2', 'id_label_1', '')])
            , Record([field('40A2', 'id_label_2', '')])
            , Record([field('40A2', 'id_label_3', '')])
            , Record([field('40A2', 'id_label_4', '')])
            , Record([field('40A2', 'id_label_5', '')])
            , Record([
                  field('1I10', 'model_type', '')  
                , field('1I10', 'analysis_type', '')
                , field('1I10', 'data_characteristic', '')
                , field('1I10', 'result_type', '')
                , field('1I10', 'data_type', '')
                , field('1I10', 'number_of_data_values', '')
            ])
            , Record([
                  field('1I10', 'design_set_id', '')
                , field('1I10', 'iteration_number', '')
                , field('1I10', 'solution_set_id', '')
                , field('1I10', 'boundary_condition', '')
                , field('1I10', 'load_set', '')
                , field('1I10', 'mode_number', '')
                , field('1I10', 'time_stamp_number', '')
                , field('1I10', 'frequency_number', '')
            ])
            , Record([ #Doc says 8 values but only two explained.
                  field('1I10', 'creation_option', '')
                , field('1I10', 'number_retained', '')
            ])
            , Record([ 
                  field('1E13.5', 'time', '')
                , field('1E13.5', 'frequency', '')
                , field('1E13.5', 'eigenvalue', '')
                , field('1E13.5', 'modal_mass', '')
                , field('1E13.5', 'viscous_damping_ratio', '')
                , field('1E13.5', 'hysteretic_damping_ratio', '')
            ])
            , Record([ 
                  field('1E13.5', 'eigenvalue_re', '')
                , field('1E13.5', 'eigenvalue_im', '')
                , field('1E13.5', 'modalA_re', '')
                , field('1E13.5', 'modalA_im', '')
                , field('1E13.5', 'modalB_re', '')
                , field('1E13.5', 'modalB_im', '')
            ])
            
        ]
        
        DataSet.__init__(self, 2414, definitionRecords, [], tokenizer)
        self.name = 'Nodes - Double Precision'
#
# Tests
#
import unittest

class TestField(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
    
        
#
if __name__ == '__main__':
    unittest.main()
    