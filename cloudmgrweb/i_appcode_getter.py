# -*- coding: UTF-8 -*-
from __future__ import with_statement
from pprint 	import pprint, pformat

import i_getter


@i_getter.define_getter( 'appcode' )
class IAppcodeGetter(
         i_getter.IGetter
      ):
    pass

if __name__ == "__main__":

   test_appcode = IAppcodeGetter( appcode = 'A01' )
   pprint( dir ( test_appcode ) )
   pprint( test_appcode.appcode )
