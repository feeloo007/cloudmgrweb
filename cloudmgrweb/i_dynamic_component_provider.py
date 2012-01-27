# -*- coding: UTF-8 -*-

from pprint import pprint

class IDynamicComponentProvider( object ):

   def __init__( self ):
      pass

   def create_dynamic_component( self, cp_id, le_create_cp ):

      le	= '__le_%s'   	% ( cp_id )
      le_prop   = 'le_%s'	% ( cp_id )
      create_cp = 'create_%s' 	% ( cp_id )
      cp_prop   = '%s'          % ( cp_id )

      def undef():
         return None

      setattr( 
         self, 
         le, 
         undef
      )

      def get_le( o ):
         return getattr( o, le )

      def set_le( o, v ):
         setattr( o, le, v )

      setattr(
         self.__class__,
         le_prop,
         property( get_le, set_le )
      )

      def create():
         local_cp = le_create_cp()

         def get_local_cp():
            return local_cp

         setattr(
            self,
            le_prop,
            get_local_cp
         )

      setattr(
         self,
         create_cp,
         create
      )

      def get_cp( o ):
         return getattr( o, le_prop )()

      setattr(
         self.__class__,
         cp_prop,
         property( get_cp )
      )

if __name__ == "__main__":
   a = IDynamicComponentProvider()
   a.create_dynamic_component( 'cp_menu_control', lambda: 'TEST' )
   pprint( dir( a ) )
   pprint( a.cp_menu_control )
   a.create_cp_menu_control()
   pprint( dir( a ) )
   pprint( a.cp_menu_control )
