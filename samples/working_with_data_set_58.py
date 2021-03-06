


import sys 
sys.path.append(r'C:\Users\ozgur\Documents\GitHub\pyUNV')
sys.path.append('./../../')

import unv 


sampleFile = '''    -1
   151
C:\Users\oy\Documents\Projects\bitbucket\UNV\data\UNVScenario.CATAnalysis       
NONE                                                                            
LMS Virtual.Lab Rev 12                                                          
                                                  
                    
LMS Virtual.Lab Rev 12                                                          
 04-May-13  09:25:32
    -1
    -1
   164
         1 SI - mks (Newton)  2
  1.00000000000000000e+00  1.00000000000000000e+00  1.00000000000000000e+00
  0.00000000000000000e+00
    -1
    -1
    58
A:+X
Function data written by LMS Virtual.Lab
04-MAY-13 09:25:32
LFS - Frequency Spectra / Default condition
Default condition
   12         1    1         0          A         1   1       NONE         0   0
         5        10         0  0.00000e+00  0.00000e+00  0.00000e+00
        18    0    0    0                 NONE                   Hz
        13    0    0    0                 NONE                    N
         0    0    0    0                 NONE                 NONE
         0    0    0    0                 NONE                 NONE
  1.00000e+01  1.10000e+00  1.20000e+00  2.00000e+01  2.10000e+00  2.20000e+00
  3.00000e+01  3.10000e+00  3.20000e+00  4.00000e+01  4.10000e+00  4.20000e+00
  5.00000e+01  5.10000e+00  5.20000e+00  6.00000e+01  6.10000e+00  6.20000e+00
  7.00000e+01  7.10000e+00  7.20000e+00  8.00000e+01  8.10000e+00  8.20000e+00
  9.00000e+01  9.10000e+00  9.20000e+00  1.00000e+02  1.01000e+01  1.02000e+01
    -1

'''


def reading_sample():
    unvFile = unv.ReadFile(sampleFile)
    print unvFile.header
    print unvFile.units 
    for dataSet in unvFile.data_sets([58]):
        print dataSet.values  
        print dataSet.data 
     

if __name__ == '__main__':
    reading_sample() 
