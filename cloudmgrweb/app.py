# -*- coding: UTF-8 -*-
from __future__ import with_statement

import os
from nagare                                     import component, presentation
from menu_control				import MenuControl
from aeras_viewer				import AerasViewer
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers

# Interactino comet
from i_comet					import ICloudMgrComet
from nagare					import ajax

# cache de component
from i_cache_components				import ICacheComponents, FormRefreshOnComet


class Cloudmgrweb( ICloudMgrResolvers, ICloudMgrComet, ICacheComponents ):
   def __init__( self ):
      ICloudMgrResolvers.__init__( self )

      # Interactino comet
      ICloudMgrComet.__init__( self )

      # cache de components
      ICacheComponents.__init__( self, cache_components = None )

      with self.cloudmap_resolver:
         self._cp_menu_control 		= component.Component( MenuControl() )
         self._cp_aeras_viewer		= component.Component( AerasViewer( le_appcode_provider = lambda: self._cp_menu_control.o.cp_appcode_selector.o.appcode, resolvers = self, cache_components = self ) )
         self._cp_form_refresh_on_comet	= component.Component( FormRefreshOnComet( cache_components = self ) )

@presentation.render_for(Cloudmgrweb)
def render(self, h, *args):

   cp_div_menu_control	        = component.Component( KnownDiv( self._cp_menu_control ) )
   cp_div_aeras_viewer	        = component.Component( KnownDiv( self._cp_aeras_viewer ) )
   cp_form_refresh_on_comet     = component.Component( KnownDiv( self._cp_form_refresh_on_comet ) )

   h.head.css_url( 'cloudmgrweb.css' )

   # Interaction comet
   h.head.javascript_url( 'cloudmgrweb_comet.js' )
   h << component.Component( self.comet_channel )

   h << component.Component( cp_form_refresh_on_comet )

   with self.cloudmap_resolver:

      with h.div( class_ = 'app' ):
         h << h.div( cp_div_menu_control, class_ = 'menu_control_struct' )
         h << h.div( cp_div_aeras_viewer, class_ = 'aeras_viewer_struct' )


   # Ajout des CallBacks
   # On le fait en fin de traitement pour que toutes les
   # knowndiv soit résolus
   self._cp_menu_control.o.cp_appcode_selector.o.register_known_div_for_appcode_change( cp_div_aeras_viewer.o )
   self._cp_menu_control.o.cp_appcode_selector.o.register_known_div_for_appcode_change( cp_div_menu_control.o.component.o.cp_menu_control_envs.o.le_get_knowndiv() )

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
