

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


def get_data_set_definition(number):
    '''data_sets_dict is a global object so we can't directly use Record and Field instances. It would 
    cause all data sets from same number to share the same record and field information which is not 
    correct, they keep the last read values themselves (perhaps if we remove that then there is no problem)
    '''
    if number in data_sets_dict:
        return data_sets_dict[number]
    else:
        return {'definition': [], 'data': []}
    
if 0:
    def get_data_set_definition(number):
        '''data_sets_dict is a global object so we can't directly use Record and Field instances. It would 
        cause all data sets from same number to share the same record and field information which is not 
        correct, they keep the last read values themselves (perhaps if we remove that then there is no problem)
        '''
        definition = {'definition': [], 'data': []}
        
        if number in data_sets_dict:
            src = data_sets_dict[number]
            srcDefRecords = src['definition']
            srcDataRecords = src['data']
            
            defRecords = definition['definition']
            dataRecords = definition['data']
            
            for srcRec in srcDefRecords:
                fields = []
                for srcField in srcRec:
                    field = Field(srcField[0], srcField[1], srcField[2], srcField[3])
                    fields.append(field)
                rec = Record(fields)
                defRecords.append(rec)
                
            for srcRec in srcDataRecords:
                fields = []
                for srcField in srcRec:
                    field = Field(srcField[0], srcField[1], srcField[2], srcField[3])
                    fields.append(field)
                rec = Record(fields)
                dataRecords.append(rec)
            
        return definition
    

    
data_sets_dict = {
      151:  {
        'definition': [
          Record([field('80A1', 'model_file_name', '')])
        , Record([field('80A1', 'model_file_description', '')])
        , Record([field('80A1', 'application_created_db', '')])
        , Record([   field('10A1', 'date_db_created', '')
            , field('1I10', 'time_db_created', '')
            , field('1I10', 'db_version', '')
            , field('1I10', 'db_subversion', '')
            , field('1I10', 'file_type', '')
          ])
        , Record([
              field('10A1', 'date_last_saved', '')
            , field('10A1', 'time_last_saved', '')
          ])
        , Record([field('80A1', 'application_created_file', '')])
        , Record([   
              field('10A1', 'date_file_created', '')
            , field('10A1', 'time_file_created', '')
            #Below are in the html but not in the record we have
            #, Field(int,  5, 'release_wrote_file', '')
            #, Field(int,  5, 'version', '')
            #, Field(int,  5, 'host_id', '')
            #, Field(int,  5, 'test_id', '')
            #, Field(int,  5, 'release_counter_per_host', '')
          ])
        ] 
        , 'data': []
      }
    , 164:  {
        'definition': [
          Record([   
              field('1I10', 'units_code', '')
            , field('20A1', 'units_desc', '')
            , field('1I10', 'temperature_mode', '')
          ])
        , Record([
              field('1D25.17', 'length', '')
            , field('1D25.17', 'force', '')
            , field('1D25.17', 'temperature', '')
            , field('1D25.17', 'temperature_offset', '')
          ])
        ]
        , 'data': []
    }
    , 2411: {
        'definition': []
        , 'data': [
              Record([   
                  field('1I10', 'node_label', '')
                , field('1I10', 'export_coordinate_system', '')
                , field('1I10', 'displacement_coordinate_system', '')
                , field('1I10', 'color', '')
              ])
            , Record([field('1P3D25.16', 'coordinate', '')])
        ]
    }
    , 2414: {
        'definition': [
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
        
        , 'data': [
                #TODO: This record has different data records based on definition. Which means
                #      we need to provide a custom class for it so it can configure its data records
                #      once the definition is read
        ]
    }
}

'''
    
data_sets_dict = {
      151:  {
        'definition': [
          [(str, 80, 'model_file_name', '')]
        , [(str, 80, 'model_file_description', '')]
        , [(str, 80, 'application_created_db', '')]
        , [   (str, 10, 'date_db_created', '')
            , (str, 10, 'time_db_created', '')
            , (int, 10, 'db_version', '')
            , (int, 10, 'db_subversion', '')
            , (int, 10, 'file_type', '')
          ]
        , [
              (str, 10, 'date_last_saved', '')
            , (str, 10, 'time_last_saved', '')
          ]
        , [(str, 80, 'application_created_file', '')]
        , [   (str, 10, 'date_file_created', '')
            , (str, 10, 'time_file_created', '')
            #Below are in the html but not in the record we have
            #, (int,  5, 'release_wrote_file', '')
            #, (int,  5, 'version', '')
            #, (int,  5, 'host_id', '')
            #, (int,  5, 'test_id', '')
            #, (int,  5, 'release_counter_per_host', '')
          ]
        ] 
        , 'data': []
      }
    , 164:  {
        'definition': [
          [   (int, 10, 'units_code', '')
            , (str, 20, 'units_desc', '')
            , (int, 10, 'temperature_mode', '')
          ]
        , [   (float, (25, 17), 'length', '')
            , (float, (25, 17), 'force', '')
            , (float, (25, 17), 'temperature', '')
            , (float, (25, 17), 'temperature_offset', '')
          ]
        ]
        , 'data': []
    }
    , 2411: {
        'definition': []
        , 'data': [
              [   (int, 10, 'node_label', '')
                , (int, 10, 'export_coordinate_system', '')
                , (int, 10, 'displacement_coordinate_system', '')
                , (int, 10, 'color', '')
              ]
              #TODO: We should support fields with multiple values
            , [
                  (float, (25, 16), 'coordinate_x', '')
                , (float, (25, 16), 'coordinate_y', '')
                , (float, (25, 16), 'coordinate_z', '')
            ]
        ]
    }
}
'''
