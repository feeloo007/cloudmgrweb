# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from menu_control_env				import MenuControlEnv
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from i_controllers                              import IAppcodeGetters


# cache de component
from i_cache_components                         import ICacheComponents

# Mise en place d'un DOM pour la gestion comet
from i_dom                                      import IDom
from i_dom_tree					import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider

from pprint					import pprint

###########################
# Vision des zones
###########################
class MenuControlEnvs( 
         ICloudMgrResolvers, 
         IAppcodeGetters, 
         ICacheComponents, 
         IDom, 
         IDomTree, 
         IDynamicComponentProvider 
      ):

   def __init__( 
          self, 
          appcode = '', 
          le_appcode_provider = None, 
          resolvers = None, 
          cache_components = None, 
          dom_storage = None, 
          dom_father = None, 
          dom_complement_element_name = '' 
       ):

      ICloudMgrResolvers.__init__( 
         self, 
         resolvers 
      )

      IAppcodeGetters.__init__( 
         self, 
         appcode = appcode, 
         le_appcode_provider = le_appcode_provider 
      )

      ICacheComponents.__init__( 
         self, 
         cache_components = cache_components 
      )

      IDynamicComponentProvider.__init__( 
         self 
      )

      # Mise en place d'un DOM pour la gestion comet
      IDom.__init__( 
         self, 
         dom_father = dom_father, 
         dom_element_name = MenuControlEnvs.__name__, 
         dom_complement_element_name = dom_complement_element_name 
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
                         cache_components = self, 
                         dom_storage = self,
                         dom_father = self, 
                         dom_complement_element_name = 'by_appcode' 
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
                                                cache_components = self, 
                                                dom_storage = self,
                                                dom_father = self, 
                                                dom_complement_element_name = 'by_appcode_by_env' 
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

      # Nettoyage du cache de composant
      self.clean_cache_for_dom( self.full_dom_element_name )

      # Suppression des précédents fils
      # dans le modèle DOM
      self.delete_dom_childs()

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
