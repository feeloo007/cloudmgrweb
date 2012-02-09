# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers
import i_getter

from counter_servers				import CounterServers

from i_dom_tree                                 import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider

from pprint					import pprint

###########################
# Vision des zones
###########################
@i_getter.define_getter( 'appcode' )
@i_getter.define_getter( 'env' )
class MenuControlEnv( 
         ICloudMgrResolvers, 
         IDomTree,
         IDynamicComponentProvider, 
      ):

   def __init__( 
          self, 
          resolvers 	= None, 
          dom_storage 	= None,
          dom_father 	= None, 
          *args,
          **kwargs
       ):

      ICloudMgrResolvers.__init__( 
         self, 
         resolvers 
      )

      IDynamicComponentProvider.__init__(
         self
      )

      IDomTree.__init__(
         self,
         dom_storage 	= dom_storage,
         dom_father 	= dom_father, 
      )

      # Définition des composants dynamiques
      def create_cp_counter_by_appcode_by_env():
         with self.cloudmap_resolver:
            return component.Component(
                      CounterServers( 
                         appcode 	= lambda: self.appcode, 
                         env 		= lambda: self.env, 
                         aera		= '*',
                         appcomp	= '*',
                         resolvers 	= self, 
                         dom_storage 	= self,
                         dom_father 	= self, 
                      ) 
                   )

      self.create_dynamic_component(
         'cp_counter_by_appcode_by_env',
         create_cp_counter_by_appcode_by_env
      )


      def create_cp_counter_by_env():
         with self.cloudmap_resolver:
            return component.Component( 
                      CounterServers( 
                         appcode	= '*',
                         env 		= lambda: self.env, 
                         aera		= '*',
                         appcomp	= '*',
                         resolvers 	= self, 
                         dom_storage 	= self,
                         dom_father 	= self, 
                      ) 
                   )
 
      self.create_dynamic_component(
         'cp_counter_by_env',
         create_cp_counter_by_env
      )


@presentation.render_for( MenuControlEnv )
def render(
       self, 
       h, 
       comp, 
       *args
    ):

   with self.cloudmap_resolver:

      # Suppression des précédents fils
      # dans le modèle DOM
      self.reset_in_dom(
              comp
      )

      # Initialisation locale des composants
      # utilisés
      self.create_cp_counter_by_appcode_by_env()
      self.create_cp_counter_by_env()

      with h.div( 
              class_='menu_control_env %s' % ( self.env ) 
           ):

         h << h.div( 
                 '%s ' % ( self.env_resolver.get_env_desc( self.env ) ), 
                 class_ = 'description' 
              )

         h << h.div( 
                 component.Component( 
                    KnownDiv( 
                       self.cp_counter_by_appcode_by_env 
                    ) 
                 ), 
                 class_ = 'counter_appcomps_struct'
              )

         h << h.div( 
                 ' / ', 
                 class_ = 'counter_appcomps_struct separator' 
              )

         h << h.div( 
                 component.Component( 
                    KnownDiv( 
                       self.cp_counter_by_env 
                    ) 
                 ), 
                 class_ = 'counter_appcomps_struct' 
              )

   return h.root

@presentation.render_for( MenuControlEnv, model = '*' )
def render(
       self, 
       h, 
       comp, 
       *args
    ):

   with self.cloudmap_resolver:

      # Suppression des précédents fils
      # dans le modèle DOM
      self.reset_in_dom(
              comp
      )

      # Initialisation locale des composants
      # utilisés
      self.create_cp_counter_by_appcode_by_env()
      self.create_cp_counter_by_env()

      with h.div( 
              class_='menu_control_env SUM' 
           ):

        h << h.div( 
                'Total ', 
                class_ = 'description' 
             )

        h << h.div( 
                 component.Component( 
                    KnownDiv( 
                       self.cp_counter_by_appcode_by_env 
                    ) 
                 ), 
                 class_ = 'counter_appcomps_struct' 
             )

        h << h.div( 
                ' / ', 
                class_ = 
                'counter_appcomps_struct separator'
             )

        h << h.div( 
                component.Component( 
                   KnownDiv( 
                      self.cp_counter_by_env 
                   ) 
                ), 
                class_ = 'counter_appcomps_struct' 
             )

   return h.root
