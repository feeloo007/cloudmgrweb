# -*- coding: UTF-8 -*-

from pprint import pprint

# Dépendance ajoutée pour tasnformer des objets
# en component supportant les KnownDIv
import nagare
import ajax_x_components

class IDynamicComponentProvider( object ):

   def __init__( self ):
      pass

   def create_dynamic_component( self, cp_id, le_create_cp ):

      le	= '__le_%s'   	% ( cp_id )
      le_prop   = 'le_%s'	% ( cp_id )
      create_cp = 'create_%s' 	% ( cp_id )
      cp_prop   = '%s'          % ( cp_id )

      setattr( 
         self, 
         le, 
         le_create_cp
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
            u'%s a supprimer' % le_create_cp.__name__
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


def cached_component_for_dom(
       self,
       component_name 		= None,
       object_class		= None.__class__,
       l_static_init_params 	= [],
       **init_params
    ):

   assert( component_name ), u'component_name dans %s.%s doit être défini' % ( __name__, cached_component_for_dom )
   assert( object_class <> None.__class__ ), u'object_class dans %s.%s doit être défini a une valeur différente de %s' % ( __name__, cached_component_for_dom, None.__class__ )

   def fct_create_component_if_needed_wrapper( fct ):

      def fct_create_component_if_needed_wrapped(
             **kwargs
          ):

          d_all_params = {}
          d_all_params.update( kwargs )
          d_all_params.update( init_params )

          o = self.get_child_with_static_init_params( 
                      object_class           = object_class,
                      l_static_init_params   = l_static_init_params, 
                      **init_params
              )

          if not o:
             o = fct(
                    l_static_init_params	= l_static_init_params,
                    **d_all_params
                 )

          return nagare.component.Component(
                    ajax_x_components.KnownDiv(
                       nagare.component.Component( 
                          o
                       )
                    )
                 )

      self.create_dynamic_component(
         component_name,
         fct_create_component_if_needed_wrapped
      )

      return fct_create_component_if_needed_wrapped

   return fct_create_component_if_needed_wrapper


if __name__ == "__main__":
   a = IDynamicComponentProvider()
   a.create_dynamic_component( 'cp_menu_control', lambda: 'TEST' )
   pprint( dir( a ) )
   pprint( a.cp_menu_control )
   a.create_cp_menu_control()
   pprint( dir( a ) )
   pprint( a.cp_menu_control )
