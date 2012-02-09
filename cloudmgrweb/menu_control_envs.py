# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from menu_control_env				import MenuControlEnv
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from i_appcode_getter                           import IAppcodeGetter


from i_dom_tree					import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider

from pprint					import pprint

###########################
# Vision des zones
###########################
class MenuControlEnvs( 
         ICloudMgrResolvers, 
         IAppcodeGetter, 
         IDomTree, 
         IDynamicComponentProvider 
      ):

   def __init__( 
          self, 
          appcode = '', 
          le_appcode_provider = None, 
          resolvers = None, 
          dom_storage = None, 
          dom_father = None, 
       ):

      ICloudMgrResolvers.__init__( 
         self, 
         resolvers 
      )

      IAppcodeGetter.__init__( 
         self, 
         appcode = appcode, 
         le_appcode_provider = le_appcode_provider 
      )

      IDynamicComponentProvider.__init__( 
         self 
      )

      IDomTree.__init__( 
         self, 
         dom_storage = dom_storage, 
         dom_father = dom_father 
      )

      # Définition des composants dynamiques
      # Filtre uniquement sur le code application
      def create_cp_menu_all_envs():
         with self.cloudmap_resolver:
            return component.Component(
                      MenuControlEnv( 
                         env = '*', 
                         le_appcode_provider = lambda: self.appcode, 
                         resolvers = self, 
                         dom_storage = self,
                         dom_father = self, 
                      ),
                      model = '*' 
                   ) 

      self.create_dynamic_component(
         'cp_menu_all_envs',
         create_cp_menu_all_envs
      )

      # filtre environnement par environnnement
      def create_d_cp_menu_by_envs():
         with self.cloudmap_resolver:
            d_cp_menu_by_envs = {}
            for env in self.env_resolver.all_envs:
               d_cp_menu_by_envs[ env ] = component.Component( 
                                             MenuControlEnv( 
                                                env = env, 
                                                le_appcode_provider = lambda: self.appcode, 
                                                resolvers = self, 
                                                dom_storage = self,
                                                dom_father = self, 
                                             ) 
                                          ) 
            return d_cp_menu_by_envs

      self.create_dynamic_component(
         'd_cp_menu_by_envs',
         create_d_cp_menu_by_envs
      )


@presentation.render_for( MenuControlEnvs )
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

      self.add_event_for_knowndiv(
         'LOCAL_REFRESH_ON_APPCODE_SELECTED',
         self,
         appcode = '*',
      )

      # Initialisation locale des composants
      # utilisés
      self.create_cp_menu_all_envs()
      self.create_d_cp_menu_by_envs()

      with h.div( 
              class_ = 'menu_control_envs' 
           ): 

         d_order = self.env_resolver.order_for_envs.copy()

         for env, cp_menu_by_env in sorted( 
                                       self.d_cp_menu_by_envs.items(), 
                                       key = lambda e: d_order[ e[ 0 ] ], 
                                       reverse = False 
                                    ):

            h << h.div( 
                    component.Component( 
                       KnownDiv( 
                         cp_menu_by_env 
                       ) 
                    ), 
                    class_ = 'menu_control_envs_struct %s' %  ( env ) 
                 )

            h << h.div( 
                    h.div, 
                    class_ = 'menu_control_envs_struct spacer' 
                 )

         h << h.div( 
                 component.Component( 
                    KnownDiv( 
                       self.cp_menu_all_envs 
                    ) 
                 ), 
                 class_ = 'menu_control_envs_struct SUM' 
              )

         h << h.div( 
                 h.div, 
                 class_ = 'menu_control_envs_struct spacer' 
              )

   return h.root
