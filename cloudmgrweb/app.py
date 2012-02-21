# -*- coding: UTF-8 -*-
from __future__ import with_statement

import os
from nagare                                     import component, presentation
from menu_control				import MenuControl
from aeras_viewer				import AerasViewer
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers
from cloudmgrlib.m_cmgr_cloudmap_resolver       import with_cloudmap_resolver

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
      # dynamique, avec un cache et avec 
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

      # Défintion du composant MenuControl
      @cached_component_for_dom(
         self,
         component_name         = 'cp_menu_control',
         object_class           = MenuControl,
         l_static_init_params   = [],
         **{ 'appcode': default_appcode, }
      )
      @with_cloudmap_resolver( self )
      def create_cp_menu_control(
             *args,
             **kwargs
          ):

         return MenuControl(
                   dom_storage     = self,
                   dom_father      = self,
                   *args,
                   **kwargs
                )

      # Défintion du composant définissant les zones
      @cached_component_for_dom(
         self,
         component_name		= 'cp_aeras_viewer',
         object_class		= AerasViewer,
         l_static_init_params 	= [],
         **{ 'appcode': default_appcode, }
      )
      @with_cloudmap_resolver( self )
      def create_cp_aeras_viewer(
             *args,
             **kwargs
          ):

         return AerasViewer(
                   resolvers             = self,
                   dom_storage           = self,
                   dom_father            = self,
                   *args,
                   **kwargs
                ) 


      # Défintion du composant permettant les mise à jour suite à un message comet
      @cached_component_for_dom(
         self,
         component_name         = 'cp_form_refresh_on_comet',
         object_class           = FormRefreshOnComet,
         l_static_init_params   = [],
         **{}
      )
      def create_cp_form_refresh_on_comet(
             *args,
             **kwargs
          ):

         return FormRefreshOnComet(
                   dom_storage        = self,
                   dom_father         = self,
                   *args,
                   **kwargs
                )


      # Défintion du composant permettant de débuger
      # lors d'un XComponentsUpdate par exemple
      @cached_component_for_dom(  
         self,
         component_name         = 'cp_debug',
         object_class           = CloudmgrwebDebug,
         l_static_init_params   = [],
         **{}
      )
      @with_cloudmap_resolver( self )
      def create_cp_debug(
             *args,
             **kwargs
          ):

         return CloudmgrwebDebug(
                   dom_storage        = self,
                   dom_father         = self,
                   cloudmgrweb        = self,
                   *args,
                   **kwargs
         )
         


@presentation.render_for(Cloudmgrweb)
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

   h << self.cp_form_refresh_on_comet

   with h.div( 
            class_ = 'app' 
        ):

      h << h.div( 
              self.cp_menu_control,
              class_ = 'menu_control_struct' 
           )

      h << h.div( 
              self.cp_aeras_viewer,
              class_ = 'aeras_viewer_struct' 
           )

   h << h.div(
           self.cp_debug
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
