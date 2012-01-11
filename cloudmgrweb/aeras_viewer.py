# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from aera_viewer				import AeraViewer
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from i_controllers				import IAppcodeGetters


###########################
# Vision des zones
###########################
class AerasViewer( ICloudMgrResolvers, IAppcodeGetters ):

   def __init__( self, appcode = '', le_appcode_provider = None, resolvers = None ):
      ICloudMgrResolvers.__init__( self, resolvers )
      IAppcodeGetters.__init__( self, appcode = appcode, le_appcode_provider = le_appcode_provider ) 

   def get_cp_aeras( self ):
      with self.cloudmap_resolver:
         self._d_cp_aeras = {}
         for aera in self.aera_resolver.all_aeras:
            self._d_cp_aeras[ aera ] = component.Component( AeraViewer( aera = aera, le_appcode_provider = lambda: self.appcode, resolvers = self ) )
      return self._d_cp_aeras
       
   cp_aeras = property( get_cp_aeras )



@presentation.render_for( AerasViewer )
def render(self, h, comp, *args):
   
   with h.div( class_ = 'aeras_viewer' ):
      if not self.appcode:
         h << h.div( u'Veuillez selectionner un code application', class_='appcodes message' )
      else:
         with self.cloudmap_resolver:
            d_order = self.aera_resolver.order_for_aeras.copy()
            for aera, cp_aera in sorted( self.cp_aeras.items(), key = lambda e: d_order[ e[ 0 ] ], reverse = False ):
               h << h.div( component.Component( KnownDiv( cp_aera ) ), class_ = 'aeras_viewer_struct %s' % aera )
               h << h.div( h.div, class_ = 'aeras_viewer_struct spacer' )
   return h.root
