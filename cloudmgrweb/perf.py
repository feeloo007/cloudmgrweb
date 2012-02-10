# -*- coding: UTF-8 -*-
import time

def timeit( method ):

   def timed( *args, **kwargs ):
      ts = time.time()
      result = method( *args, **kwargs )
      te = time.time()

      print '%r (%r, %r) %2.4f' % ( method.__name__, args, kwargs, te - ts )

      return result

   return timed
