# -*- coding: UTF-8 -*-
from __future__ import with_statement
from pprint	import pprint

###########################
# Vision des zones
###########################
class IDom( object ):

   def __init__( self, dom_father = None, dom_element_name = '' ):
      self._dom_father 		= dom_father
      self._dom_element_name 	= dom_element_name

   def get_dom_element_name( self ):
      return self._dom_element_name
   dom_element_name = property( get_dom_element_name )

   def get_full_dom_element_name( self ):
      result = None
      f = self.dom_father

      if f:
         result = '%s/%s' % ( f.full_dom_element_name, self.dom_element_name )
      else:
         result = '/%s' % ( self.dom_element_name )

      return result

   full_dom_element_name = property( get_full_dom_element_name )

   def get_dom_father( self ):
      return self._dom_father
   dom_father = property( get_dom_father ) 
