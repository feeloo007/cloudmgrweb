# -*- coding: UTF-8 -*-
from __future__ import with_statement

import os
from nagare                                     import component, presentation
from appcode_selector				import AppcodeSelector
from aeras_viewer				import AerasViewer
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers

class Cloudmgrweb( ICloudMgrResolvers ):
   def __init__( self ):
      ICloudMgrResolvers.__init__( self )
      with self.cloudmap_resolver:
         self._cp_appcode_selector 	= component.Component( AppcodeSelector() )
         self._cp_aeras_viewer	= component.Component( AerasViewer( le_appcode_provider = lambda: self._cp_appcode_selector.o.appcode, resolvers = self ) )

@presentation.render_for(Cloudmgrweb)
def render(self, h, *args):

   cp_div_appcode_selector	= component.Component( KnownDiv( self._cp_appcode_selector ) )
   cp_div_aeras_viewer	        = component.Component( KnownDiv( self._cp_aeras_viewer ) )
   self._cp_appcode_selector.o.register_known_div_for_appcode_change( cp_div_aeras_viewer.o )

   h.head.css_url( 'cloudmgrweb.css' )

   with self.cloudmap_resolver:

      with h.div( class_ = 'app', id_ = 'app' ):
         h << h.div( cp_div_appcode_selector, id_ = 'appcode_selector_struct' )
         h << h.div( cp_div_aeras_viewer, id = 'aeras_viewer_struct' )

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
