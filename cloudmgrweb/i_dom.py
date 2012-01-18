# -*- coding: UTF-8 -*-
from __future__ import with_statement
from pprint	import pprint

###########################
# Vision des zones
###########################
class IDom( object ):

   def __init__( self, father = None, dom_element_name = '' ):
      self._father 		= father
      self._dom_element_name 	= dom_element_name

   def get_dom_element_name( self ):
      return self._dom_element_name
   dom_element_name = property( get_dom_element_name )

   def get_full_dom_element_name( self ):
      result = '/%s' % ( self.dom_element_name )
      f = self._father
      while f:
         result = '%s/%s' % ( result, f.full_dom_element_name )
      return result
   full_dom_element_name = property( get_full_dom_element_name )
