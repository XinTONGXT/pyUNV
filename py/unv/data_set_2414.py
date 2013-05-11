

__author__ = "Ozgur Yuksel (ozgur@insequor.com)"
__copyright__ = "Copyright (C) 2013 Ozgur Yuksel"
__license__ = "TBD"
__version__ = "0.0"

__doc__ = ''' '''


# Standard

# 3rd Party

# Internal
from common import make_options
from unv_tokenizer import data_folder
from unv_data_set import DataSet, Record, Tokenizer
from unv_field import Field

    
#Custom Fields
DataSetLocationOptions = '''1:    Data at nodes
                                   2:    Data on elements
                                   3:    Data at nodes on elements
                                   5:    Data at points
                                   6:    Data on elements at nodes'''
DataSetLocationOptions = make_options(DataSetLocationOptions, int, ':')

ModelTypeOptions = '''0:   Unknown
                                   1:   Structural
                                   2:   Heat transfer
                                   3:   Fluid flow'''
ModelTypeOptions = make_options(ModelTypeOptions, int, ':')   
                                
AnalysisTypeOptions = '''0:   Unknown
                                   1:   Static
                                   2:   Normal mode
                                   3:   Complex eigenvalue first order
                                   4:   Transient
                                   5:   Frequency response
                                   6:   Buckling
                                   7:   Complex eigenvalue second order
                                   9:   Static non-linear
                                  10:   Craig-Bampton constraint modes
                                  11:   Equivalent attachment modes
                                  12:   Effective mass modes
                                  13:   Effective mass matrix
                                  14:   Effective mass matrix
                                  15:   Distributed Load Load Distribution
                                  16:   Distributed Load Attachment modes'''                      
AnalysisTypeOptions = make_options(AnalysisTypeOptions, int, ':')
                                  
DataCharacteristicOptions = '''0:   Unknown
                                   1:   Scalar
                                   2:   3 DOF global translation vector
                                   3:   6 DOF global translation & rotation vector
                                   4:   Symmetric global tensor
                                   6:   Stress resultants'''
                                   
DataCharacteristicOptions = make_options(DataCharacteristicOptions, int, ':')

ResultTypeOptions = '''2:Stress
                                   3:Strain
                                   4:Element Force
                                   5:Temperature
                                   6:Heat Flux
                                   7:Strain Energy
                                   8:Displacement
                                   9:Reaction Force
                                  10:Kinetic Energy
                                  11:Velocity
                                  12:Acceleration
                                  13:Strain Energy Density
                                  14:Kinetic Energy Density
                                  15:Hydrostatic Pressure
                                  16:Heat Gradient
                                  17:Code Check Value
                                  18:Coefficient of Pressure
                                  19:Ply Stress
                                  20:Ply Strain
                                  21:Failure Index for Ply
                                  22:Failure Index for Bonding
                                  23:Reaction Heat Flow
                                  24:Stress Error Density
                                  25:Stress Variation
                                  27:Element Stress Resultant
                                  28:Length
                                  29:Area
                                  30:Volume
                                  31:Mass
                                  32:Constraint Force
                                  34:Plastic Strain
                                  35:Creep Strain
                                  36:Strain Energy Error Norm
                                  37:Dynamic Stress At Nodes
                                  38:Heat Transfer Coefficient
                                  39:Temperature Gradient
                                  40:Kinetic Energy Dissipation Rate
                                  41:Strain Energy Error
                                  42:Mass Flow
                                  43:Mass Flux
                                  44:Heat Flow
                                  45:View Factor
                                  46:Heat Load
                                  47:Stress Component
                                  48:Green Strain
                                  49:Contact Forces
                                  50:Contact Pressure
                                  51:Contact Stress
                                  52:Contact Friction Stress
                                  53:Velocity Component
                                  54:Heat Flux Component
                                  55:Infrared Heat Flux
                                  56:Diffuse Solar Heat Flux
                                  57:Collimated Solar Heat Flux
                                  58:Safety Factor
                                  59:Fatigue Damage
                                  60:Fatigue Damage With Direction
                                  61:Fatigue Life                      
                                  62:Quality Index
                                  63:Stress With Direction
                                  64:Translation With Direction
                                  65:Rotation With Direction
                                  66:Force With Direction
                                  67:Moment With Direction
                                  68:Translational Acceleration With Dir
                                  69:Rotational Acceleration With Direction
                                  70:Level Crossing Rate With Direction
                                  71:Trans Shell Stress Resultant With Dir
                                  72:Rot Shell Stress Resultant With Dir
                                  73:Failure Index 
                                  74:Level Crossing Rate
                                  75:Displacement Component
                                  76:Acceleration Component
                                  77:Force Component
                                  78:Strain Component
                                  94:Unknown Scalar
                                  95:Unknown 3DOF Vector
                                  96:Unknown 6DOF Vector
                                  97:Unknown Symmetric Tensor
                                  98:Unknown General Tensor
                                  99:Unknown Stress Resultant
                                 101:Gap Thickness
                                 102:Solid Layer (+ surface)
                                 103:Solid Layer (- surface)
                                 104:Total Solid Layer
                                 105:Flow Vector at Fill
                                 106:Bulk Flow Vector
                                 107:Core Displacement
                                 108:Layered Shear Strain Rate
                                 109:Shear Stress
                                 110:Heat Flux (+ surface)
                                 111:Heat Flux (- surface)
                                 112:Layered Temperature
                                 113:Bulk Temperature
                                 114:Peak Temperature
                                 115:Temperature at Fill
                                 116:Mass Density
                                 117:Pressure
                                 118:Volumetric Skrinkage
                                 119:Filling Time
                                 120:Ejection Time
                                 121:No-flow Time
                                 122:Weld Line Meeting Angle
                                 123:Weld Line Underflow
                                 124:Original Runner Diameter
                                 125:Optimized Runner Diameter
                                 126:Change in Runner Diameter
                                 127:Averaged Layered Cure
                                 128:Layered Cure
                                 129:Cure Rate
                                 130:Cure Time
                                 131:Induction Time
                                 132:Temperature at Cure
                                 133:Percent Gelation
                                 134:Part Heat Flux (+ surface)
                                 135:Part Heat Flux (- surface)
                                 136:Part-Wall Temperature (+ surface)
                                 137:Part-Wall Temperature (- surface)
                                 138:Part Ejection Time
                                 139:Part Peak Temperature
                                 140:Part Average Temperature
                                 141:Parting Temperature (+ surface)
                                 142:Parting Temperature (- surface)
                                 143:Parting Heat Flux (- surface)
                                 144:Parting Heat Flux (+ surface)
                                 145:Wall Temperature Convergence
                                 146:Wall Temperature (- surface)
                                 147:Wall Temperature (+ surface)
                                 148:Line Heat Flux
                                 149:Line Pressure
                                 150:Reynold's Number
                                 151:Line Film Coefficient
                                 152:Line Temperature
                                 153:Line Bulk Temperature
                                 154:Mold Temperature
                                 155:Mold Heat Flux
                                 156:Rod Heater Temperature
                                 157:Rod Heater Flux
                                 158:Original Line Diameter
                                 159:Optimized Line Diameter
                                 160:Change in Line Diameter
                                 161:Air Traps
                                 162:Weld Lines
                                 163:Injection Growth
                                 164:Temp Diff (Celcius)
                                 165:Shear Rate
                                 166:Viscosity
                                 167:Percentage
                                 168:Time
                                 169:Flow Direction
                                 170:Speed
                                 171:Flow Rate
                                 172:Thickness Ratio
                                 201:Maximum Temperature
                                 202:Minimum Temperature
                                 203:Time of Maximum Temperature
                                 204:Time of Minimum Temperature
                                 205:Conductive Flux
                                 206:Total Flux
                                 207:Residuals
                                 208:View Factor Sum
                                 209:Velocity Adjusted
                                 210:Pressure (+ surface)
                                 211:Pressure (- surface)
                                 212:Static Pressure
                                 213:Total Pressure
                                 214:K-E Turbulence Energy
                                 215:K-E Turbulence Dissipation
                                 216:Fluid Density
                                 217:Shear Stress (+ surface)
                                 218:Shear Stress (- surface)
                                 219:Roughness (+ surface)
                                 220:Roughness (- surface)
                                 221:Y+ (+ surface)
                                 222:Y+ (- surface)
                                 223:Fluid Temperature
                                 224:Convective Heat Flux
                                 225:Local Convection Coefficient
                                 226:Bulk Convection Coefficient
                                 301:Sound Pressure
                                 302:Sound Power
                                 303:Sound Intensity
                                 304:Sound Energy
                                 305:Sound Energy Density''' #>1000:  User defined result type
                                 
                                
ResultTypeOptions = make_options(ResultTypeOptions, int, ':')

DataTypeOptions = '''1:   Integer
                                   2:   Single precision floating point
                                   4:   Double precision floating point
                                   5:   Single precision complex
                                   6:   Double precision complex'''
                                   
DataTypeOptions = make_options(DataTypeOptions, int, ':')

#
#
class DataSet2414 (DataSet):
    def __init__(self, tokenizer):
        definitionRecords = [
              Record([Field(format='1I10', name='label')], 'dataset')
            , Record([Field(format='40A2', name='name')], 'dataset')
            , Record([Field(format='1I10', name='location', options=DataSetLocationOptions)], 'dataset')
            , Record([Field(format='40A2', name=1)], 'id_lines')
            , Record([Field(format='40A2', name=2)], 'id_lines')
            , Record([Field(format='40A2', name=3)], 'id_lines')
            , Record([Field(format='40A2', name=4)], 'id_lines')
            , Record([Field(format='40A2', name=5)], 'id_lines')
            , Record([ #Record 9
                  Field(format='1I10', name='model_type', options=ModelTypeOptions)  
                , Field(format='1I10', name='analysis_type', options=AnalysisTypeOptions)
                , Field(format='1I10', name='data_characteristic', options=DataCharacteristicOptions)
                , Field(format='1I10', name='result_type', options=ResultTypeOptions)
                , Field(format='1I10', name='data_type', options=DataTypeOptions)
                , Field(format='1I10', name='number_of_data_values')
            ])
            , Record([ #Record 10
                  Field(format='1I10', name='design_set_id')
                , Field(format='1I10', name='iteration_number')
                , Field(format='1I10', name='solution_set_id')
                , Field(format='1I10', name='boundary_condition')
                , Field(format='1I10', name='load_set')
                , Field(format='1I10', name='mode_number')
                , Field(format='1I10', name='time_stamp_number')
                , Field(format='1I10', name='frequency_number')
            ])
            , Record([ #Record 11, Doc says 8 values but only two explained.
                  Field(format='1I10', name='creation_option')
                , Field(format='1I10', name='number_retained1')
                , Field(format='1I10', name='number_retained2')
                , Field(format='1I10', name='number_retained3')
                , Field(format='1I10', name='number_retained4')
                , Field(format='1I10', name='number_retained5')
                , Field(format='1I10', name='number_retained6')
                , Field(format='1I10', name='number_retained7')
            ])
            , Record([ #Record 12
                  Field(format='1E13.5', name='time')
                , Field(format='1E13.5', name='frequency')
                , Field(format='1E13.5', name='eigenvalue')
                , Field(format='1E13.5', name='modal_mass')
                , Field(format='1E13.5', name='viscous_damping_ratio')
                , Field(format='1E13.5', name='hysteretic_damping_ratio')
            ])
            , Record([ #Record 13
                  Field(format='1E13.5', name='eigenvalue_re')
                , Field(format='1E13.5', name='eigenvalue_im')
                , Field(format='1E13.5', name='modalA_re')
                , Field(format='1E13.5', name='modalA_im')
                , Field(format='1E13.5', name='modalB_re')
                , Field(format='1E13.5', name='modalB_im')
            ])
            
        ]    
        DataSet.__init__(self, 2414, definitionRecords, [], tokenizer)
        self.name = 'Analysis Data'
        
    def read_definition(self):
        '''
        '''
        values = DataSet.read_definition(self)
        
        records = []
        if values.dataset.location == 1: #Data At Nodes
            records.append(Record([Field(format='1E13.5', name='node_number')]))
            fields = []
            
            if values.data_type == 5: #Single Precision, Complex
                format = 'C13.5'
            if values.data_characteristic == 3: #3 * Translation + 3 * Rotation
                format = 'P3' + format
                fields.append(Field(format=format, name='translation'))
                fields.append(Field(format=format, name='rotation'))
            
            if len(fields) > 0:
                records.append(Record(fields))
            
        self.data_records = records
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
            dataSet = DataSet2414(tokenizer)
            self.assertEquals(len(dataSet.definition_records), 13)
            self.assertEquals(len(dataSet.data_records), 0)
    
    #
    def test_DataSetReadsDefinition(self):
        with Tokenizer(open(data_folder + '2414_structural_mode_single_precision_complex.unv', 'r')) as tokenizer:
            dataSet = DataSet2414(tokenizer)
            values = dataSet.values;
            if 1: #Records 1 to 8
                self.assertEquals(values.dataset.label, 1)
                self.assertEquals(values.dataset.name, 'Exported by LMS: Modal data: nodal complex translation and rotation')
                self.assertEquals(values.dataset.location, 1)
                self.assertEquals(values.dataset.location_, 'Data at nodes')
                #...
                self.assertEquals(values.id_lines[2], 'Data written by LMS Virtual.Lab')
            
            if 1: #Record 9
                self.assertEquals(values.model_type, 1)
                self.assertEquals(values.model_type_, 'Structural')
                
                self.assertEquals(values.analysis_type, 2)
                self.assertEquals(values.analysis_type_, 'Normal mode')
                
                self.assertEquals(values.data_characteristic, 3)
                self.assertEquals(values.data_characteristic_, '6 DOF global translation & rotation vector')
                
                self.assertEquals(values.result_type, 8)
                self.assertEquals(values.result_type_, 'Displacement')
                
                self.assertEquals(values.data_type, 5)
                self.assertEquals(values.data_type_, 'Single precision complex')
                
                self.assertEquals(values.number_of_data_values, 6)
            
            if 1: #Record 10 and 11
                self.assertEquals(values.design_set_id, 0)
                self.assertEquals(values.iteration_number, 0)
                self.assertEquals(values.solution_set_id, 29291)
                self.assertEquals(values.boundary_condition, 0)
                self.assertEquals(values.load_set, 0)
                self.assertEquals(values.mode_number, 1)
                self.assertEquals(values.time_stamp_number, 0)
                self.assertEquals(values.frequency_number, 0)
                self.assertEquals(values.creation_option, 0)
            
            if 1: #Record 12 and 13
                self.assertEquals(values.time, 0.0)
                self.assertEquals(values.frequency, 8.29173e+00)
                self.assertEquals(values.eigenvalue, 0.0)
                self.assertEquals(values.modal_mass, 1.0)
                self.assertEquals(values.viscous_damping_ratio, 3.05439e-03)
                self.assertEquals(values.hysteretic_damping_ratio, 0.0)
                self.assertEquals(values.eigenvalue_re, -1.59130e-01)
                self.assertEquals(values.eigenvalue_im, 5.20985e+01)
                self.assertEquals(values.modalA_re, 1.0)
                self.assertEquals(values.modalA_im, 0.0)
                self.assertEquals(values.modalB_re, 0.0)
                self.assertEquals(values.modalB_im, 0.0)
            
    def test_DataSetInitializedDataRecordsForSinglePrecisionComplexWith6DOF(self):
        with Tokenizer(open(data_folder + '2414_structural_mode_single_precision_complex.unv', 'r')) as tokenizer:
            dataSet = DataSet2414(tokenizer)
            values = dataSet.read_definition()
            self.assertEquals(len(dataSet.data_records), 2)
            
            data = dataSet.read_data()
            self.assertEqual(len(data), values.number_of_data_values)
            
            for i in range(len(data)):
                self.assertEqual(data[i].node_number, i + 1)
            
            #Just test the first and the last value
            self.assertEqual(data[0].translation[0], complex(-1.58112e-03,  0.00000e+00))
            self.assertEqual(data[len(data) - 1].rotation[2], complex(1.17549e-38,  1.17549e-38))
            
            
#
if __name__ == '__main__':
    unittest.main()
    