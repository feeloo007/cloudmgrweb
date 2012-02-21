# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import component, presentation
from appcode_selector				import AppcodeSelector
from menu_control_envs	 			import MenuControlEnvs
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers
from cloudmgrlib.m_cmgr_cloudmap_resolver       import with_cloudmap_resolver

import i_getter

# Mise en place d'un DOM pour la gestion comet
from i_dom_tree					import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider, cached_component_for_dom

from pprint					import pprint

@i_getter.define_getter( 'appcode' )
class MenuControl( 
         ICloudMgrResolvers, 
         IDomTree, 
         IDynamicComponentProvider 
      ):
   def __init__( 
          self, 
          dom_storage 	= None, 
          dom_father 	= None, 
          *args,
          **kwargs
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
         dom_storage 	= dom_storage, 
         dom_father 	= dom_father 
      )

      # Définition des composants dynamiques
      # Menu de controle
      @cached_component_for_dom(
         self,
         component_name         = 'cp_appcode_selector',
         object_class           = AppcodeSelector,
         l_static_init_params   = [],
         **{ 'appcode': self.appcode, }
      )
      @with_cloudmap_resolver( self )
      def create_cp_appcode_selector(
             *args,
             **kwargs
          ):
         return component.Component(
            AppcodeSelector(
               dom_storage 	= self,
               dom_father 	= self,
               *args,
               **kwargs
            )
         )


      @cached_component_for_dom(
         self,
         component_name         = 'cp_menu_control_envs',
         object_class           = MenuControlEnvs,
         l_static_init_params   = [],
         **{ 'appcode': self.appcode, }
      )
      @with_cloudmap_resolver( self )
      def create_cp_menu_control_envs(
             *args,
             **kwargs
          ):
         return component.Component(
                   MenuControlEnvs(
                      resolvers 	= self,
                      dom_storage 	= self,
                      dom_father 	= self,
                      *args,
                      **kwargs
                   )
                )


@presentation.render_for(MenuControl)
@with_cloudmap_resolver()
def render(
       self, 
       h, 
       comp,
       *args,
       **kwargs
    ):


   # Suppression des précédents fils
   # dans le modèle DOM
   self.reset_in_dom(
           comp
   )

   with h.div( 
           class_ = 'menu_control' 
        ):

      h << h.div( 
              self.cp_appcode_selector,
              class_ = 'menu_control_struct APPCODE' 
           )

      h << h.div( 
              '', 
              class_ = 'menu_control_struct spacer' 
           )

      h << h.div( 
              self.cp_menu_control_envs, 
              class_ = 'menu_control_struct ENVS' 
           )

   return h.root
