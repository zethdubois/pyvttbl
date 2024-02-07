from __future__ import print_function

# Copyright (c) 2011, Roger Lew [see LICENSE.txt]
# This software is funded in part by NIH Grant P20 RR016454.

import unittest
import warnings
import os
import math
from random import shuffle, random
from collections import Counter,OrderedDict
from pyvttbl.misc.dictset import DictSet,_rep_generator
from math import isnan, isinf, floor
import numpy as np
from pprint import pprint as pp

from pyvttbl import PyvtTbl
from pyvttbl import DataFrame
from pyvttbl.plotting import *
from pyvttbl.stats import *
from pyvttbl.misc.support import *

class Test_anova_transform(unittest.TestCase):
    def test1(self):
        ## Within test with Windsor transformation
        R = """\
WINDSOR05_ERROR ~ TIMEOFDAY * COURSE * MODEL

TESTS OF WITHIN SUBJECTS EFFECTS

Measure: WINDSOR05_ERROR
     Source                              Type III    eps     df       MS         F         Sig.      et2_G   Obs.    SE     95% CI    lambda     Obs.  
                                            SS                                                                                                   Power 
======================================================================================================================================================
TIMEOFDAY           Sphericity Assumed    130.667       -       1   130.667     92.235       0.019   3.698     27   0.622    1.218    1512.000       1 
                    Greenhouse-Geisser    130.667       1       1   130.667     92.235       0.019   3.698     27   0.622    1.218    1512.000       1 
                    Huynh-Feldt           130.667       1       1   130.667     92.235       0.019   3.698     27   0.622    1.218    1512.000       1 
                    Box                   130.667       1       1   130.667     92.235       0.019   3.698     27   0.622    1.218    1512.000       1 
------------------------------------------------------------------------------------------------------------------------------------------------------
Error(TIMEOFDAY)    Sphericity Assumed      2.333       -   1.647     1.417                                                                            
                    Greenhouse-Geisser      2.333       1   1.647     1.417                                                                            
                    Huynh-Feldt             2.333       1   1.647     1.417                                                                            
                    Box                     2.333       1   1.647     1.417                                                                            
------------------------------------------------------------------------------------------------------------------------------------------------------
COURSE              Sphericity Assumed     51.370       -       2    25.685   1142.235   2.087e-05   1.454     18   0.055    0.107   12483.000       1 
                    Greenhouse-Geisser     51.370   0.501   1.003    51.229   1142.235       0.002   1.454     18   0.055    0.107   12483.000       1 
                    Huynh-Feldt            51.370   0.506   1.011    50.810   1142.235       0.002   1.454     18   0.055    0.107   12483.000       1 
                    Box                    51.370   0.500       1    51.370   1142.235       0.002   1.454     18   0.055    0.107   12483.000       1 
------------------------------------------------------------------------------------------------------------------------------------------------------
Error(COURSE)       Sphericity Assumed      0.074       -   3.294     0.022                                                                            
                    Greenhouse-Geisser      0.074   0.501   1.652     0.045                                                                            
                    Huynh-Feldt             0.074   0.506   1.665     0.044                                                                            
                    Box                     0.074   0.500   1.647     0.045                                                                            
------------------------------------------------------------------------------------------------------------------------------------------------------
MODEL               Sphericity Assumed     47.148       -       2    23.574    123.336   8.004e-04   1.334     18   0.159    0.312    1347.882       1 
                    Greenhouse-Geisser     47.148   0.504   1.008    46.773    123.336       0.015   1.334     18   0.159    0.312    1347.882   1.000 
                    Huynh-Feldt            47.148   0.516   1.032    45.671    123.336       0.014   1.334     18   0.159    0.312    1347.882   1.000 
                    Box                    47.148   0.500       1    47.148    123.336       0.015   1.334     18   0.159    0.312    1347.882   1.000 
------------------------------------------------------------------------------------------------------------------------------------------------------
Error(MODEL)        Sphericity Assumed      0.630       -   3.294     0.191                                                                            
                    Greenhouse-Geisser      0.630   0.504   1.660     0.379                                                                            
                    Huynh-Feldt             0.630   0.516   1.700     0.370                                                                            
                    Box                     0.630   0.500   1.647     0.382                                                                            
------------------------------------------------------------------------------------------------------------------------------------------------------
TIMEOFDAY *         Sphericity Assumed      5.444       -       2     2.722      1.834       0.292   0.154      9   0.627    1.229      10.023   0.410 
COURSE              Greenhouse-Geisser      5.444   0.720   1.441     3.779      1.834       0.313   0.154      9   0.627    1.229      10.023   0.302 
                    Huynh-Feldt             5.444   0.933   1.867     2.916      1.834       0.296   0.154      9   0.627    1.229      10.023   0.385 
                    Box                     5.444   0.500       1     5.444      1.834       0.332   0.154      9   0.627    1.229      10.023   0.217 
------------------------------------------------------------------------------------------------------------------------------------------------------
Error(TIMEOFDAY *   Sphericity Assumed      4.889       -   3.294     1.484                                                                            
COURSE)             Greenhouse-Geisser      4.889   0.720   2.373     2.060                                                                            
                    Huynh-Feldt             4.889   0.933   3.075     1.590                                                                            
                    Box                     4.889   0.500   1.647     2.968                                                                            
------------------------------------------------------------------------------------------------------------------------------------------------------
TIMEOFDAY *         Sphericity Assumed     14.333       -       2     7.167     70.824       0.002   0.406      9   0.164    0.321     387.000   1.000 
MODEL               Greenhouse-Geisser     14.333   0.511   1.023    14.011     70.824       0.023   0.406      9   0.164    0.321     387.000   0.998 
                    Huynh-Feldt            14.333   0.520   1.040    13.776     70.824       0.022   0.406      9   0.164    0.321     387.000   0.998 
                    Box                    14.333   0.500       1    14.333     70.824       0.024   0.406      9   0.164    0.321     387.000   0.997 
------------------------------------------------------------------------------------------------------------------------------------------------------
Error(TIMEOFDAY *   Sphericity Assumed      0.333       -   3.294     0.101                                                                            
MODEL)              Greenhouse-Geisser      0.333   0.511   1.685     0.198                                                                            
                    Huynh-Feldt             0.333   0.520   1.714     0.195                                                                            
                    Box                     0.333   0.500   1.647     0.202                                                                            
------------------------------------------------------------------------------------------------------------------------------------------------------
COURSE *            Sphericity Assumed      8.296       -       4     2.074      3.804       0.064   0.235      6   0.368    0.722      13.856   0.545 
MODEL               Greenhouse-Geisser      8.296   0.327   1.307     6.347      3.804       0.188   0.235      6   0.368    0.722      13.856   0.211 
                    Huynh-Feldt             8.296   0.327   1.307     6.347      3.804       0.188   0.235      6   0.368    0.722      13.856   0.211 
                    Box                     8.296   0.500       2     4.148      3.804       0.139   0.235      6   0.368    0.722      13.856   0.304 
------------------------------------------------------------------------------------------------------------------------------------------------------
Error(COURSE *      Sphericity Assumed      3.593       -   6.588     0.545                                                                            
MODEL)              Greenhouse-Geisser      3.593   0.327   2.153     1.669                                                                            
                    Huynh-Feldt             3.593   0.327   2.153     1.669                                                                            
                    Box                     3.593   0.500   3.294     1.091                                                                            
------------------------------------------------------------------------------------------------------------------------------------------------------
TIMEOFDAY *         Sphericity Assumed      2.222       -       4     0.556      1.318       0.355   0.063      3   0.458    0.898       2.400   0.125 
COURSE *            Greenhouse-Geisser      2.222   0.336   1.343     1.654      1.318       0.387   0.063      3   0.458    0.898       2.400   0.080 
MODEL               Huynh-Feldt             2.222   0.336   1.343     1.654      1.318       0.387   0.063      3   0.458    0.898       2.400   0.080 
                    Box                     2.222   0.500       2     1.111      1.318       0.380   0.063      3   0.458    0.898       2.400   0.093 
------------------------------------------------------------------------------------------------------------------------------------------------------
Error(TIMEOFDAY *   Sphericity Assumed      2.778       -   6.588     0.422                                                                            
COURSE *            Greenhouse-Geisser      2.778   0.336   2.212     1.256                                                                            
MODEL)              Huynh-Feldt             2.778   0.336   2.212     1.256                                                                            
                    Box                     2.778   0.500   3.294     0.843                                                                            

TABLES OF ESTIMATED MARGINAL MEANS

Estimated Marginal Means for TIMEOFDAY
TIMEOFDAY   Mean    Std. Error   95% Lower Bound   95% Upper Bound 
==================================================================
T1          5.704        0.433             4.855             6.552 
T2          2.593        0.215             2.171             3.014 

Estimated Marginal Means for COURSE
COURSE   Mean    Std. Error   95% Lower Bound   95% Upper Bound 
===============================================================
C1       5.167        0.584             4.021             6.312 
C2       4.444        0.532             3.403             5.486 
C3       2.833        0.414             2.021             3.645 

Estimated Marginal Means for MODEL
MODEL   Mean    Std. Error   95% Lower Bound   95% Upper Bound 
==============================================================
M1      5.222        0.645             3.959             6.485 
M2      4.278        0.535             3.229             5.327 
M3      2.944        0.328             2.301             3.588 

Estimated Marginal Means for TIMEOFDAY * COURSE
TIMEOFDAY   COURSE   Mean    Std. Error   95% Lower Bound   95% Upper Bound 
===========================================================================
T1          C1       7.111        0.588             5.959             8.263 
T1          C2           6        0.726             4.576             7.424 
T1          C3           4        0.577             2.868             5.132 
T2          C1       3.222        0.401             2.437             4.007 
T2          C2       2.889        0.261             2.378             3.400 
T2          C3       1.667        0.236             1.205             2.129 

Estimated Marginal Means for TIMEOFDAY * MODEL
TIMEOFDAY   MODEL   Mean    Std. Error   95% Lower Bound   95% Upper Bound 
==========================================================================
T1          M1      7.222        0.760             5.733             8.711 
T1          M2      6.111        0.512             5.107             7.115 
T1          M3      3.778        0.465             2.867             4.689 
T2          M1      3.222        0.434             2.372             4.073 
T2          M2      2.444        0.338             1.782             3.107 
T2          M3      2.111        0.261             1.600             2.622 

Estimated Marginal Means for COURSE * MODEL
COURSE   MODEL   Mean    Std. Error   95% Lower Bound   95% Upper Bound 
=======================================================================
C1       M1      6.500        0.992             4.556             8.444 
C1       M2      5.167        1.195             2.825             7.509 
C1       M3      3.833        0.601             2.656             5.011 
C2       M1          6        1.095             3.853             8.147 
C2       M2      4.167        0.792             2.614             5.720 
C2       M3      3.167        0.477             2.231             4.102 
C3       M1      3.167        0.872             1.457             4.877 
C3       M2      3.500        0.764             2.003             4.997 
C3       M3      1.833        0.307             1.231             2.436 

Estimated Marginal Means for TIMEOFDAY * COURSE * MODEL
TIMEOFDAY   COURSE   MODEL   Mean    Std. Error   95% Lower Bound   95% Upper Bound 
===================================================================================
T1          C1       M1      8.667        0.333             8.013             9.320 
T1          C1       M2      7.667        0.333             7.013             8.320 
T1          C1       M3          5        0.577             3.868             6.132 
T1          C2       M1      8.333        0.667             7.027             9.640 
T1          C2       M2      5.667        0.882             3.938             7.395 
T1          C2       M3          4        0.577             2.868             5.132 
T1          C3       M1      4.667        1.202             2.311             7.022 
T1          C3       M2          5        0.577             3.868             6.132 
T1          C3       M3      2.333        0.333             1.680             2.987 
T2          C1       M1      4.333        0.333             3.680             4.987 
T2          C1       M2      2.667        0.882             0.938             4.395 
T2          C1       M3      2.667        0.333             2.013             3.320 
T2          C2       M1      3.667        0.333             3.013             4.320 
T2          C2       M2      2.667        0.333             2.013             3.320 
T2          C2       M3      2.333        0.333             1.680             2.987 
T2          C3       M1      1.667        0.333             1.013             2.320 
T2          C3       M2          2        0.577             0.868             3.132 
T2          C3       M3      1.333        0.333             0.680             1.987 

"""
        
        df=DataFrame()
        fname='data/error~subjectXtimeofdayXcourseXmodel.csv'
        df.read_tbl(fname)
        aov=df.anova('ERROR',wfactors=['TIMEOFDAY','COURSE','MODEL'],transform='windsor05')
##        print(aov)
        self.assertEqual(str(aov),R)

            
def suite():
    return unittest.TestSuite((
            unittest.makeSuite(Test_anova_transform)
                              ))

if __name__ == "__main__":
    # run tests
    runner = unittest.TextTestRunner()
    runner.run(suite())
    
