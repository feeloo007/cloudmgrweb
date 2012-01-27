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

# cache de component
from i_cache_components				import ICacheComponents, FormRefreshOnComet

# Mise en place d'un DOM pour la gestion comet
from i_dom					import IDom
from i_dom_tree					import IDomTree

from i_dynamic_component_provider		import IDynamicComponentProvider	

from pprint					import pprint

from debug 					import CloudmgrwebDebug

class Cloudmgrweb( 
         ICloudMgrResolvers, 
         ICloudMgrComet, 
         ICacheComponents, 
         IDom, 
         IDomTree, 
         IDynamicComponentProvider 
      ):

   def __init__(
          self 
      ):

      ICloudMgrResolvers.__init__( 
         self 
      )

      # Interaction comet
      ICloudMgrComet.__init__(
         self
      )

      # cache de components
      ICacheComponents.__init__( 
         self,
         cache_components = None 
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
         dom_father = None, 
         dom_element_name = Cloudmgrweb.__name__ 
      )

      IDomTree.__init__( 
         self, 
         dom_storage = None, 
         dom_father = None 
      )

      # Définition des composants dynamiques
      # Menu de controle
      def create_cp_menu_control():
         with self.cloudmap_resolver:
            return component.Component(
               MenuControl(
                  dom_storage = self,
                  dom_father = self,
                  cache_components = self,
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
                         le_appcode_provider = lambda: self.cp_menu_control.o.cp_appcode_selector.o.appcode,
                         resolvers = self,
                         dom_storage = self,
                         dom_father = self,
                         cache_components = self,
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
                      cache_components = self,
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
                      cache_components  = self,
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
       *args
    ):

   with self.cloudmap_resolver:

      # Suppression des précédents fils
      # dans le modèle DOM
      self.delete_dom_childs()

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

      # Ajout des CallBacks
      # On le fait en fin de traitement pour que toutes les
      # knowndiv soit résolus
      self.cp_menu_control.o.cp_appcode_selector.o.register_known_div_for_appcode_change( 
         cp_div_aeras_viewer.o
      )

      self.cp_menu_control.o.cp_appcode_selector.o.register_known_div_for_appcode_change( 
         cp_div_menu_control.o.component.o.cp_menu_control_envs.o.le_get_knowndiv() 
      )


      self.cp_menu_control.o.cp_appcode_selector.o.register_known_div_for_appcode_change(
         cp_div_debug.o
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
