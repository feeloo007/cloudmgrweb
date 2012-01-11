# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers
from envs_viewer				import EnvsViewer
from i_controllers                              import IAppcodeGetters, IAeraGetters

###########################
# Vision des zones
###########################
class AeraViewer( ICloudMgrResolvers, IAppcodeGetters, IAeraGetters ):

   def __init__( self, aera = '', le_aera_provider = None, appcode = '', le_appcode_provider = None, resolvers = None ):
      ICloudMgrResolvers.__init__( self, resolvers )
      IAppcodeGetters.__init__( self, appcode = appcode, le_appcode_provider = le_appcode_provider )
      IAeraGetters.__init__( self, aera = aera, le_aera_provider = le_aera_provider )

      with self.cloudmap_resolver:
         self._cp_envs_viewer = component.Component( EnvsViewer( le_appcode_provider = lambda: self.appcode, le_aera_provider = lambda: self.aera, resolvers = self ) )

@presentation.render_for( AeraViewer )
def render(self, h, comp, *args):
   with self.cloudmap_resolver:
      with h.div( class_='aera_viewer %s' % ( self.aera ) ):
         h << h.div( self.aera_resolver.get_aera_desc( self.aera ), class_ = 'description' )
         h << h.div( component.Component( KnownDiv( self._cp_envs_viewer ) ), class_ = 'aera %s' % ( self.aera ) )
   return h.root
