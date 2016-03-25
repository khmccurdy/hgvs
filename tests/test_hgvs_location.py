# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from nose.plugins.attrib import attr

from hgvs.exceptions import HGVSError, HGVSUnsupportedOperationError
import hgvs.location


@attr(tags=["quick", "models"])
class Test_SimplePosition(unittest.TestCase):
    def test_success(self):
        self.assertEqual(str(hgvs.location.SimplePosition(5)), '5')
        self.assertEqual(str(hgvs.location.SimplePosition(5, uncertain=True)), '(5)')
        self.assertEqual(str(hgvs.location.SimplePosition(None)), '?')

    def test_failure(self):
        with self.assertRaises(AssertionError):
            self.assertEqual(hgvs.location.SimplePosition(-1), 'SHOULD FAIL')

    def test_simple_subtraction(self):
        self.assertEqual(
            hgvs.location.SimplePosition(5) - hgvs.location.SimplePosition(3),
            2)


@attr(tags=["quick"])
class Test_BaseOffsetPosition(unittest.TestCase):
    def test_success(self):
        # r.5
        cdsp = hgvs.location.BaseOffsetPosition(5)
        self.assertEqual(cdsp.datum, hgvs.location.SEQ_START)
        self.assertEqual(cdsp.base, 5)
        self.assertEqual(cdsp.offset, 0)
        self.assertEqual(str(cdsp), '5')

        #r.5+6
        cdsp.offset = 6
        self.assertEqual(str(cdsp), '5+6')

        #r.5+?
        cdsp.offset = None
        self.assertEqual(str(cdsp), '5+?')

        #r.(5+?)
        cdsp.uncertain = True
        self.assertEqual(str(cdsp), '(5+?)')

        # c.*5
        cdsp = hgvs.location.BaseOffsetPosition(5, datum=hgvs.location.CDS_END)
        self.assertEqual(cdsp.datum, hgvs.location.CDS_END)
        self.assertEqual(cdsp.base, 5)
        self.assertEqual(cdsp.offset, 0)
        self.assertEqual(str(cdsp), '*5')

        cdsp.uncertain = True
        self.assertEqual(str(cdsp), '(*5)')

        cdsp.offset = 7
        self.assertEqual(str(cdsp), '(*5+7)')


    def test_baseoffset_subtraction(self):
        v30 = hgvs.location.BaseOffsetPosition(3,0)
        v50 = hgvs.location.BaseOffsetPosition(5,0)
        v52 = hgvs.location.BaseOffsetPosition(5,2)
        v54 = hgvs.location.BaseOffsetPosition(5,4)

        self.assertEqual(v50-v30, 2)
        
        with self.assertRaises(HGVSError):
            _ = v54-v52
        with self.assertRaises(HGVSError):
            _ = v54-v30

        


@attr(tags=["quick"])
class Test_AAPosition(unittest.TestCase):
    def test_AAPosition(self):
        ap = hgvs.location.AAPosition(15, 'S')
        self.assertEqual(ap.pos, 15)
        self.assertEqual(str(ap), 'Ser15')

    def test_aaposition_subtraction(self):
        l1 = hgvs.location.AAPosition(15, 'S')
        l2 = hgvs.location.AAPosition(20, 'S')
        self.assertEqual(l2-l1, 5)


@attr(tags=["quick"])
class Test_Interval(unittest.TestCase):
    def test_Interval(self):
        ival = hgvs.location.Interval(hgvs.location.BaseOffsetPosition(base=12,
                                                                       offset=+34),
                                      hgvs.location.BaseOffsetPosition(base=56,
                                                                       offset=-78))
        self.assertEqual(ival.start.base, 12)
        self.assertEqual(ival.start.offset, 34)
        self.assertEqual(ival.end.base, 56)
        self.assertEqual(ival.end.offset, -78)
        self.assertEqual(str(ival), '12+34_56-78')

    def test_length(self):
        ival = hgvs.location.Interval(hgvs.location.BaseOffsetPosition(base=12,
                                                                       offset=0),
                                      hgvs.location.BaseOffsetPosition(base=50,
                                                                       offset=0))
        self.assertEqual(ival._length(), 39)


if __name__ == '__main__':
    unittest.main()


## <LICENSE>
## Copyright 2014 HGVS Contributors (https://bitbucket.org/biocommons/hgvs)
## 
## Licensed under the Apache License, Version 2.0 (the "License");
## you may not use this file except in compliance with the License.
## You may obtain a copy of the License at
## 
##     http://www.apache.org/licenses/LICENSE-2.0
## 
## Unless required by applicable law or agreed to in writing, software
## distributed under the License is distributed on an "AS IS" BASIS,
## WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
## See the License for the specific language governing permissions and
## limitations under the License.
## </LICENSE>
