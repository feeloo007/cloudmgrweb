# -*- coding: UTF-8 -*-
from __future__ import with_statement

import os
from nagare                                     import component, presentation
from menu_control				import MenuControl
from aeras_viewer				import AerasViewer
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers

# Interaction comet
from i_comet					import ICloudMgrComet

from form_refresh_on_comet			import FormRefreshOnComet

# Mise en place d'un DOM pour la gestion comet
from i_dom_tree					import IDomTree

from i_dynamic_component_provider		import IDynamicComponentProvider, cached_component_for_dom

from pprint					import pprint, pformat

from debug 					import CloudmgrwebDebug

from colorama					import Fore, Back, Style


class Cloudmgrweb( 
         ICloudMgrResolvers, 
         ICloudMgrComet, 
         IDomTree, 
         IDynamicComponentProvider 
      ):

   def __init__(
          self,
          l_static_init_params = [],
          *args,
          **kwargs
      ):

      default_appcode = 'L01'


      ICloudMgrResolvers.__init__( 
         self 
      )

      # Interaction comet
      ICloudMgrComet.__init__(
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
         dom_storage 		= None, 
         dom_father 		= None,
         l_static_init_params	= l_static_init_params,
         **kwargs
      )

      # Définition des composants dynamiques
      # Menu de controle
      def create_cp_menu_control():
         with self.cloudmap_resolver:
            return component.Component(
                      KnownDiv(
                         component.Component(
                            MenuControl(
                               appcode 		= default_appcode,
                               dom_storage 	= self,
                               dom_father 	= self,
                            )
                         )
                      )
                   )

      self.create_dynamic_component( 
         'cp_menu_control', 
         create_cp_menu_control
      )


      # Défintion du composant définissant les zones
      init_params 		= {
                                     'appcode': default_appcode,
                    		  }

      l_static_init_params 	= []

      @cached_component_for_dom(
         self,
         component_name		= 'cp_aeras_viewer',
         object_class		= AerasViewer,
         l_static_init_params 	= l_static_init_params,
         **init_params
      )
      def create_cp_aeras_viewer(
             **kwargs
          ):
         with self.cloudmap_resolver:
            return AerasViewer(
                      resolvers             = self,
                      dom_storage           = self,
                      dom_father            = self,
                      **kwargs
                   ) 

      # Formulaire pour les rechargements
      # suite à un message comet
      def create_cp_form_refresh_on_comet():
         return component.Component(
                   KnownDiv(
                      component.Component(
                         FormRefreshOnComet(
                            dom_storage	= self,
                            dom_father 	= self,
                         )
                      )
                   )
                )

      self.create_dynamic_component(
         'cp_form_refresh_on_comet',
         create_cp_form_refresh_on_comet
      ) 


      def create_cp_debug():
         return component.Component(
                   KnownDiv(
                      component.Component(
                         CloudmgrwebDebug(
                            dom_storage	= self,
                            dom_father 	= self,
                            cloudmgrweb	= self,
                         )
                      )
                   )
                )

      self.create_dynamic_component(
         'cp_debug',
         create_cp_debug,
      )


@presentation.render_for(Cloudmgrweb)
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
      #self.create_cp_menu_control()
      #self.create_cp_aeras_viewer()
      #self.create_cp_form_refresh_on_comet()
      #self.create_cp_debug()

      # Création des DIV
      #cp_div_menu_control	   = self.cp_menu_control 

      cp_div_aeras_viewer	   = self.cp_aeras_viewer

      #cp_div_form_refresh_on_comet = self.cp_form_refresh_on_comet 

      #cp_div_debug                 = self.cp_debug

      # Rendu
      h.head.css_url( 
         'cloudmgrweb.css' 
      )

      # Interaction comet
      h.head.javascript_url( 
         'cloudmgrweb_comet.js' 
      )

      #h << component.Component( 
      #        self.comet_channel 
      #     )

      #h << cp_div_form_refresh_on_comet

      ## DEBUG ##
      ## VVVVV ##
      with h.form:
         h << h.input( type = 'submit', value = 'recharger' )
      ## ^^^^^ ##
      ## DEBUG ##

      with h.div( 
               class_ = 'app' 
           ):

         #h << h.div( 
         #        cp_div_menu_control, 
         #        class_ = 'menu_control_struct' 
         #     )

         h << h.div( 
                 cp_div_aeras_viewer, 
                 class_ = 'aeras_viewer_struct' 
              )

      #h << h.div(
      #        cp_div_debug
      #     )

      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br
      h << h.br

   return h.root

# ---------------------------------------------------------------

app = Cloudmgrweb
