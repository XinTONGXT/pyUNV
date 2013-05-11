

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
from unv_field import Field

    
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
              Record([Field(format='80A1', name=1)], 'id_lines')
            , Record([Field(format='80A1', name=2)], 'id_lines')
            , Record([Field(format='80A1', name=3)], 'id_lines')
            , Record([Field(format='80A1', name=4)], 'id_lines')
            , Record([Field(format='80A1', name=5)], 'id_lines')
            , Record(name='dof', fields=[ #Record 6:     Format(2(I5,I10),2(1X,10A1,I10,I4))
                  Field(format='1I5' , name='function_type', options= FunctionTypeOptions)
                , Field(format='1I10', name='function_id')
                , Field(format='1I5' , name='sequence_number')
                , Field(format='1I10', name='load_case_id', options=LoadCaseIDOptions)
                , Field(format='1X')
                , Field(format='10A1', name='response_entity_name')
                , Field(format='1I10', name='response_node')
                , Field(format='1I4' , name='response_direction', options=ResponseDirectionOptions)
                , Field(format='1X')
                , Field(format='10A1', name='reference_entity_name')
                , Field(format='1I10', name='reference_node')
                , Field(format='1I4' , name='reference_direction', options=ResponseDirectionOptions)
                     ])
            , Record(name='data', fields=[ #Record 7:     Format(3I10,3E13.5)
                          Field(format='1I10'  , name='ordinate_data_type', options=OrdinateDataTypeOptions)
                        , Field(format='1I10'  , name='number_of_data_points')
                        , Field(format='1I10'  , name='abscissa_spacing', options=AbscissaSpacingOptions)
                        , Field(format='1E13.5', name='abscissa_minimum')
                        , Field(format='1E13.5', name='abscissa_increment')
                        , Field(format='1E13.5', name='z_axis_value')
                     ])
            , Record(name='abscissa', fields=[ #Record 8:     Format(I10,3I5,2(1X,20A1))
                          Field(format='1I10', name='data_type', options=AbscissaDataTypeOptions)
                        , Field(format='1I5' , name='length_units_exponent')
                        , Field(format='1I5' , name='force_units_exponent')
                        , Field(format='1I5' , name='temperature_units_exponent')
                        , Field(format='1X')
                        , Field(format='20A1', name='axis_label')
                        , Field(format='1X')
                        , Field(format='20A1', name='axis_units_label')
                     ])
            , Record(name='ordinate_numerator', fields=[ #Record 9:     Format(I10,3I5,2(1X,20A1))
                          Field(format='1I10', name='data_type', options=AbscissaDataTypeOptions)
                        , Field(format='1I5' , name='length_units_exponent')
                        , Field(format='1I5' , name='force_units_exponent')
                        , Field(format='1I5' , name='temperature_units_exponent')
                        , Field(format='1X')
                        , Field(format='20A1', name='axis_label')
                        , Field(format='1X')
                        , Field(format='20A1', name='axis_units_label')
                     ])
            , Record(name='ordinate_denominator', fields=[ #Record 10:    Format(I10,3I5,2(1X,20A1))
                          Field(format='1I10', name='data_type', options=AbscissaDataTypeOptions)
                        , Field(format='1I5' , name='length_units_exponent')
                        , Field(format='1I5' , name='force_units_exponent')
                        , Field(format='1I5' , name='temperature_units_exponent')
                        , Field(format='1X')
                        , Field(format='20A1', name='axis_label')
                        , Field(format='1X')
                        , Field(format='20A1', name='axis_units_label')
                     ])
            , Record(name='z_axis', fields=[ #Record 11:    Format(I10,3I5,2(1X,20A1))
                          Field(format='1I10', name='data_type')
                        , Field(format='1I5' , name='length_units_exponent')
                        , Field(format='1I5' , name='force_units_exponent')
                        , Field(format='1I5' , name='temperature_units_exponent')
                        , Field(format='1X')
                        , Field(format='20A1', name='axis_label')
                        , Field(format='1X')
                        , Field(format='20A1', name='axis_units_label')
                     ])
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
            fields.append(Field(format='1E13.5', name='abscissa'))
        if  values.data.ordinate_data_type == 2:
            fields.append(Field(format='1E13.5', name='value'))
        elif values.data.ordinate_data_type == 4:
            fields.append(Field(format='1E20.12', name='value'))
        elif values.data.ordinate_data_type == 5:
            fields.append(Field(format='1P2E13.5', name='value'))
        elif values.data.ordinate_data_type == 6:
            fields.append(Field(format='1P2E20.12', name='value'))
        
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
    