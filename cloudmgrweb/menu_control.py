# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import component, presentation
from appcode_selector				import AppcodeSelector
from menu_control_envs	 			import MenuControlEnvs
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers

# cache de component
from i_cache_components				import ICacheComponents

# Mise en place d'un DOM pour la gestion comet
from i_dom                                      import IDom

from i_dom_tree					import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider

from pprint					import pprint


class MenuControl( 
         ICloudMgrResolvers, 
         ICacheComponents, 
         IDom, 
         IDomTree, 
         IDynamicComponentProvider 
      ):
   def __init__( 
          self, 
          dom_storage = None, 
          dom_father = None, 
          dom_complement_element_name = '', 
          cache_components = None 
       ):

      ICloudMgrResolvers.__init__( 
         self 
      )

      # cache de components
      ICacheComponents.__init__( 
         self, 
         cache_components = cache_components 
      )

      # Création de l'interface
      # permettant la génération
      # des composants de manière
      # dynamique et avec 
      # alimentation de l'objet en proprerties
      IDynamicComponentProvider.__init__( 
         self 
      )

      # Mise en place d'un DOM pour la gestion comet
      IDom.__init__( 
         self, 
         dom_father = dom_father, 
         dom_element_name = MenuControl.__name__, 
         dom_complement_element_name = dom_complement_element_name 
      )

      IDomTree.__init__( 
         self, 
         dom_storage = dom_storage, 
         dom_father = dom_father 
      )

      # Définition des composants dynamiques
      # Menu de controle
      def create_cp_appcode_selector():
         with self.cloudmap_resolver:
            return component.Component(
               AppcodeSelector()
            )

      self.create_dynamic_component(
         'cp_appcode_selector',
         create_cp_appcode_selector,
      )

      def create_cp_menu_control_envs():
         with self.cloudmap_resolver:
            return component.Component(
                      MenuControlEnvs(
                         le_appcode_provider = lambda: self.cp_appcode_selector.o.appcode,
                         resolvers = self,
                         cache_components = self,
                         dom_storage = self,
                         dom_father = self,
                      )
                   )

      self.create_dynamic_component(
         'cp_menu_control_envs',
         create_cp_menu_control_envs,
      ) 
      
@presentation.render_for(MenuControl)
def render(
       self, 
       h, 
       *args
    ):


   with self.cloudmap_resolver:

      # Suppression des précédents fils
      # dans le modèle DOM
      self.delete_dom_childs()

      # Initialisation locale des composants
      # utilisés
      self.create_cp_appcode_selector()
      self.create_cp_menu_control_envs()

      # Création des DIV
      cp_div_appcode_selector	= component.Component( 
                                     KnownDiv( 
                                        self.cp_appcode_selector 
                                     ) 
                                  )

      cp_div_menu_control_envs	= component.Component( 
                                     KnownDiv( 
                                        self.cp_menu_control_envs 
                                     ) 
                                  )

      # Interaction comet
      with self.cloudmap_resolver:

         with h.div( 
                 class_ = 'menu_control' 
              ):

            h << h.div( 
                    cp_div_appcode_selector,
                    class_ = 'menu_control_struct APPCODE' 
                 )

            h << h.div( 
                    '', 
                    class_ = 'menu_control_struct spacer' 
                 )

            h << h.div( 
                    cp_div_menu_control_envs, 
                    class_ = 'menu_control_struct ENVS' 
                 )

   return h.root
