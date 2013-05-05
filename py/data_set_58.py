

__author__ = "Ozgur Yuksel (ozgur@insequor.com)"
__copyright__ = "Copyright (C) 2013 Ozgur Yuksel"
__license__ = "TBD"
__version__ = "0.0"

__doc__ = '''Dataset Definition for ID=58, function data
Idea with a specific dataset record is to:
- Configure the data set record
- Customize the behavior when necessary. For example record 58 might 
have different data records based on the definition information, so 
as soon as definition is in place we should configure the data values
'''


# Standard

# 3rd Party

# Internal
from unv_data_set import DataSet, Record, Tokenizer
from unv_field import field, Field

    
#Custom Fields
#Record 6
FunctionTypeOptions = '''0 - General or Unknown
    1 - Time Response
    2 - Auto Spectrum
    3 - Cross Spectrum
    4 - Frequency Response Function
    5 - Transmissibility
    6 - Coherence
    7 - Auto Correlation
    8 - Cross Correlation
    9 - Power Spectral Density (PSD)
    10 - Energy Spectral Density (ESD)
    11 - Probability Density Function
    12 - Spectrum
    13 - Cumulative Frequency Distribution
    14 - Peaks Valley
    15 - Stress/Cycles
    16 - Strain/Cycles
    17 - Orbit
    18 - Mode Indicator Function
    19 - Force Pattern
    20 - Partial Power
    21 - Partial Coherence
    22 - Eigenvalue
    23 - Eigenvector
    24 - Shock Response Spectrum
    25 - Finite Impulse Response Filter
    26 - Multiple Coherence
    27 - Order Function
    28 - Phase Compensation'''

LoadCaseIDOptions = '''0 - Single Point Excitation'''

ResponseDirectionOptions = '''0 - Scalar
     1 - +X Translation       
     4 - +X Rotation
    -1 - -X Translation      
    -4 - -X Rotation
     2 - +Y Translation       
     5 - +Y Rotation
    -2 - -Y Translation      
    -5 - -Y Rotation
     3 - +Z Translation       
     6 - +Z Rotation
    -3 - -Z Translation      
    -6 - -Z Rotation'''
#Record 7
OrdinateDataTypeOptions = '''2 - real, single precision
    4 - real, double precision
    5 - complex, single precision
    6 - complex, double precision'''
        
AbscissaSpacingOptions = '''0 - uneven
    1 - even (no abscissa values stored)'''

#Record 8
AbscissaDataTypeOptions = '''0 - unknown
    1 - general
    2 - stress
    3 - strain
    5 - temperature
    6 - heat flux
    8 - displacement
    9 - reaction force
    11 - velocity
    12 - acceleration
    13 - excitation force
    15 - pressure
    16 - mass
    17 - time
    18 - frequency
    19 - rpm
    20 - order
    21 - sound pressure
    22 - sound intensity
    23 - sound power'''    
#
#
class DataSet58 (DataSet):
    def __init__(self, tokenizer):
        definitionRecords = [
              Record([field('80A1', 1, '')], 'id_lines')
            , Record([field('80A1', 2, '')], 'id_lines')
            , Record([field('80A1', 3, '')], 'id_lines')
            , Record([field('80A1', 4, '')], 'id_lines')
            , Record([field('80A1', 5, '')], 'id_lines')
            , Record([ #Record 6:     Format(2(I5,I10),2(1X,10A1,I10,I4))
                          field('1I5' , 'function_type', '', FunctionTypeOptions)
                        , field('1I10', 'function_id', '')
                        , field('1I5' , 'sequence_number', '')
                        , field('1I10', 'load_case_id', '', LoadCaseIDOptions)
                        , field('1X'  , ' ', '')
                        , field('10A1', 'response_entity_name', '')
                        , field('1I10', 'response_node', '')
                        , field('1I4' , 'response_direction', '', ResponseDirectionOptions)
                        , field('1X'  , ' ', '')
                        , field('10A1', 'reference_entity_name', '')
                        , field('1I10', 'reference_node', '')
                        , field('1I4' , 'reference_direction', '', ResponseDirectionOptions)
                     ], 'dof')
            , Record([ #Record 7:     Format(3I10,3E13.5)
                          field('1I10'  , 'ordinate_data_type', '', OrdinateDataTypeOptions)
                        , field('1I10'  , 'number_of_data_points', '')
                        , field('1I10'  , 'abscissa_spacing', '', AbscissaSpacingOptions)
                        , field('1E13.5', 'abscissa_minimum', '')
                        , field('1E13.5', 'abscissa_increment', '')
                        , field('1E13.5', 'z_axis_value', '')
                     ], 'data')
            , Record([ #Record 8:     Format(I10,3I5,2(1X,20A1))
                          field('1I10', 'data_type', '', AbscissaDataTypeOptions)
                        , field('1I5' , 'length_units_exponent', '')
                        , field('1I5' , 'force_units_exponent', '')
                        , field('1I5' , 'temperature_units_exponent', '')
                        , field('1X'  , '', '')
                        , field('20A1', 'axis_label', '')
                        , field('1X'  , '', '')
                        , field('20A1', 'axis_units_label', '')
                     ], 'abscissa')
            , Record([ #Record 9:     Format(I10,3I5,2(1X,20A1))
                          field('1I10', 'data_type', '', AbscissaDataTypeOptions)
                        , field('1I5' , 'length_units_exponent', '')
                        , field('1I5' , 'force_units_exponent', '')
                        , field('1I5' , 'temperature_units_exponent', '')
                        , field('1X'  , '', '')
                        , field('20A1', 'axis_label', '')
                        , field('1X'  , '', '')
                        , field('20A1', 'axis_units_label', '')
                     ], 'ordinate_numerator')
            , Record([ #Record 10:    Format(I10,3I5,2(1X,20A1))
                          field('1I10', 'data_type', '', AbscissaDataTypeOptions)
                        , field('1I5' , 'length_units_exponent', '')
                        , field('1I5' , 'force_units_exponent', '')
                        , field('1I5' , 'temperature_units_exponent', '')
                        , field('1X'  , '', '')
                        , field('20A1', 'axis_label', '')
                        , field('1X'  , '', '')
                        , field('20A1', 'axis_units_label', '')
                     ], 'ordinate_denominator')
            , Record([ #Record 11:    Format(I10,3I5,2(1X,20A1))
                          field('1I10', 'data_type', '')
                        , field('1I5' , 'length_units_exponent', '')
                        , field('1I5' , 'force_units_exponent', '')
                        , field('1I5' , 'temperature_units_exponent', '')
                        , field('1X'  , '', '')
                        , field('20A1', 'axis_label', '')
                        , field('1X'  , '', '')
                        , field('20A1', 'axis_units_label', '')
                     ], 'z_axis')
        ]
        DataSet.__init__(self, 58, definitionRecords, [], tokenizer)
        self.name = 'Function at Nodal DOF'
        
    def read_definition(self):
        '''Data record format of this data set depends on two fields in definition:
           1. Record 7.ordinate_data_type:
                2 - real, single precision
                4 - real, double precision
                5 - complex, single precision
                6 - complex, double precision
           2. Record 7. abscissa_spacing:
                0 - uneven
                1 - even (no abscissa values stored)
                
                          Ordinate            Abscissa
             Case     Type     Precision     Spacing       Format
           -------------------------------------------------------------
               1      real      single        even         6E13.5       ? 1
               2      real      single       uneven        6E13.5       ? 2
               3     complex    single        even         6E13.5       ? 2
               4     complex    single       uneven        6E13.5       ? 3
               5      real      double        even         4E20.12      ? 1
               6      real      double       uneven     2(E13.5,E20.12) ? 1
               7     complex    double        even         4E20.12      ? 2
               8     complex    double       uneven      E13.5,2E20.12    OK
           --------------------------------------------------------------
        '''
        values = DataSet.read_definition(self)
        fields = []
        if values.data.abscissa_spacing == 0:
            fields.append(field('1E13.5', 'abscissa', ''))
        if  values.data.ordinate_data_type == 2:
            fields.append(field('1E13.5', 'value', ''))
        elif values.data.ordinate_data_type == 4:
            fields.append(field('1E20.12', 'value', ''))
        elif values.data.ordinate_data_type == 5:
            fields.append(field('1P2E13.5', 'value', ''))
        elif values.data.ordinate_data_type == 6:
            fields.append(field('1P2E20.12', 'value', ''))
        
        self.data_records = [Record(fields)]
        
        if 0:
            print '\n'
            for v in values: 
                print v
                for k in values[v]:
                    print '   ', k, '=', values[v][k]
            
        return values
        
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
    def test_DataSetIsStartedWithEmptyDataRecords(self):
        with Tokenizer('') as tokenizer:
            dataSet = DataSet58(tokenizer)
            self.assertEquals(len(dataSet.definition_records), 11)
            self.assertEquals(len(dataSet.data_records), 0)
            
    #
    def test_DataSetReadsDefinition(self):
        with Tokenizer(open('../data/58_real_data_with_argument.unv', 'r')) as tokenizer:
            dataSet = DataSet58(tokenizer)
            self.assertEquals(dataSet.values.id_lines[1], 'Force_Time:+X')
            #...
            self.assertEquals(dataSet.values.id_lines[5], 'Default condition')
            #Record 6
            self.assertEquals(dataSet.values.dof.function_type, 1)
            self.assertEquals(dataSet.values.dof.response_entity_name, 'Force_Time')
            #Record 7
            self.assertEquals(dataSet.values.data.ordinate_data_type, 2)
            self.assertEquals(dataSet.values.data.number_of_data_points, 10)
            #Record 8
            self.assertEquals(dataSet.values.abscissa.data_type, 17)
            self.assertEquals(dataSet.values.abscissa.axis_units_label, 's')
            #Record 9
            self.assertEquals(dataSet.values.ordinate_numerator.data_type, 13)
            self.assertEquals(dataSet.values.ordinate_numerator.axis_units_label, 'N')
            #Record 10
            self.assertEquals(dataSet.values.ordinate_denominator.data_type, 0)
            self.assertEquals(dataSet.values.ordinate_denominator.axis_units_label, 'NONE')
            #Record 11
            self.assertEquals(dataSet.values.z_axis.data_type, 0)
            self.assertEquals(dataSet.values.z_axis.axis_units_label, 'NONE')
            
    #
    def test_DataSetInitializedDataRecordsForRealSingleDataWithArguents(self):
        with Tokenizer(open('../data/58_real_data_with_argument.unv', 'r')) as tokenizer:
            dataSet = DataSet58(tokenizer)
            values = dataSet.read_definition()
            self.assertEquals(len(dataSet.data_records), 1)
            
            data = dataSet.read_data()
            
            for i in range(values.data.number_of_data_points):
                self.assertEqual(data[i].abscissa, 10.0 * (i + 1))
                self.assertEqual(data[i].value,   1.0 * (i + 1) + 0.1)
                
    #
    def test_DataSetInitializedDataRecordsForComplexSingleDataWithArguents(self):
        with Tokenizer(open('../data/58_complex_data_with_argument.unv', 'r')) as tokenizer:
            dataSet = DataSet58(tokenizer)
            values = dataSet.read_definition()
            self.assertEquals(len(dataSet.data_records), 1)
            
            data = dataSet.read_data()
            
            for i in range(values.data.number_of_data_points):
                self.assertEqual(data[i].abscissa, 10.0 * (i + 1))
                self.assertEqual(data[i].value,   [1.0 * (i + 1) + 0.1, 1.0 * (i + 1) + 0.2])
            
        
#
if __name__ == '__main__':
    unittest.main()
    