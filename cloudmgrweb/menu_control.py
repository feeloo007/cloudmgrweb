# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import component, presentation
from appcode_selector				import AppcodeSelector
from menu_control_envs	 			import MenuControlEnvs
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers

# Mise en place d'un DOM pour la gestion comet
from i_dom_tree					import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider

from pprint					import pprint


class MenuControl( 
         ICloudMgrResolvers, 
         IDomTree, 
         IDynamicComponentProvider 
      ):
   def __init__( 
          self, 
          dom_storage = None, 
          dom_father = None, 
       ):

      ICloudMgrResolvers.__init__( 
         self 
      )

      # Création de l'interface
      # permettant la génération
      # des composants de manière
      # dynamique et avec 
      # alimentation de l'objet en proprerties
      IDynamicComponentProvider.__init__( 
         self 
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
               AppcodeSelector(
                  dom_storage 	= self,
                  dom_father 	= self,
               )
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
