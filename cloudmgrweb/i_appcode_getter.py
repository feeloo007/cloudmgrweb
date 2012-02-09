# -*- coding: UTF-8 -*-
from __future__ import with_statement
from pprint 	import pprint, pformat

from i_getter 	import *


@define_accessor( 'appcode' )
class IAppcodeGetter(
         IGetters
      ):
    pass

if __name__ == "__main__":

   test_appcode = IAppcodeGetter( appcode = 'A01' )
   pprint( dir ( test_appcode ) )
   pprint( test_appcode.appcode )
