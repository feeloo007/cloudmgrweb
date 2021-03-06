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

from i_dynamic_component_provider		import IDynamicComponentProvider	

from pprint					import pprint, pformat

from debug 					import CloudmgrwebDebug


class Cloudmgrweb( 
         ICloudMgrResolvers, 
         ICloudMgrComet, 
         IDomTree, 
         IDynamicComponentProvider 
      ):

   def __init__(
          self,
      ):

      default_appcode = ''


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
         dom_storage 	= None, 
         dom_father 	= None 
      )

      # Définition des composants dynamiques
      # Menu de controle
      def create_cp_menu_control():
         with self.cloudmap_resolver:
            return component.Component(
               MenuControl(
                  appcode 	= default_appcode,
                  dom_storage 	= self,
                  dom_father 	= self,
               )
            )

      self.create_dynamic_component( 
         'cp_menu_control', 
         create_cp_menu_control
      )

      # affichage des zones
      def create_cp_aeras_viewer():
         with self.cloudmap_resolver:
            return component.Component( 
                      AerasViewer(
                         appcode 	= default_appcode,
                         resolvers 	= self,
                         dom_storage 	= self,
                         dom_father 	= self,
                      )
                   )

      self.create_dynamic_component(
         'cp_aeras_viewer',
         create_cp_aeras_viewer
      ) 

      # Formulaire pour les rechargements
      # suite à un message comet
      def create_cp_form_refresh_on_comet():
         return component.Component(
                   FormRefreshOnComet(
                      dom_storage 	= self,
                      dom_father 	= self,
                   )
                )

      self.create_dynamic_component(
         'cp_form_refresh_on_comet',
         create_cp_form_refresh_on_comet
      ) 


      def create_cp_debug():
         return component.Component(
                   CloudmgrwebDebug(
                      dom_storage       = self,
                      dom_father        = self,
                      cloudmgrweb	= self,
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
      self.create_cp_menu_control()
      self.create_cp_aeras_viewer()
      self.create_cp_form_refresh_on_comet()
      self.create_cp_debug()

      # Création des DIV
      cp_div_menu_control	   = component.Component( 
                                        KnownDiv( 
                                           self.cp_menu_control 
                                        ) 
                                     )

      cp_div_aeras_viewer	   = component.Component( 
                                        KnownDiv(
                                           self.cp_aeras_viewer 
                                        ) 
                                     )

      cp_div_form_refresh_on_comet = component.Component( 
                                        KnownDiv( 
                                           self.cp_form_refresh_on_comet 
                                        ) 
                                     )

      cp_div_debug                 = component.Component(
                                        KnownDiv(
                                           self.cp_debug
                                        )
                                     )

      # Rendu
      h.head.css_url( 
         'cloudmgrweb.css' 
      )

      # Interaction comet
      h.head.javascript_url( 
         'cloudmgrweb_comet.js' 
      )

      h << component.Component( 
              self.comet_channel 
           )

      h << cp_div_form_refresh_on_comet

      with h.div( 
               class_ = 'app' 
           ):

         h << h.div( 
                 cp_div_menu_control, 
                 class_ = 'menu_control_struct' 
              )

         h << h.div( 
                 cp_div_aeras_viewer, 
                 class_ = 'aeras_viewer_struct' 
              )

      h << h.div(
              cp_div_debug
           )

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
