# -*- coding: UTF-8 -*-
from __future__ import with_statement
from pprint 	import pprint, pformat

import i_getter 



@i_getter.define_getter( 'env' )
class IEnvGetter(
         i_getter.IGetter
      ):
    pass
