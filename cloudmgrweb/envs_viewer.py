# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from env_viewer					import EnvViewer
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from i_controllers                              import IAppcodeGetters, IAeraGetters

###########################
# Vision des zones
###########################
class EnvsViewer( ICloudMgrResolvers, IAppcodeGetters, IAeraGetters ):

   def __init__( self, appcode = '', le_appcode_provider = None, aera = '', le_aera_provider = None, resolvers = None ):
      ICloudMgrResolvers.__init__( self, resolvers )
      IAppcodeGetters.__init__( self, appcode = appcode, le_appcode_provider = le_appcode_provider )
      IAeraGetters.__init__( self, aera = aera, le_aera_provider= le_aera_provider )

   def get_cp_envs( self ):
      with self.cloudmap_resolver:
         self._d_cp_envs = {}
         for env in self.env_resolver.all_envs:
            self._d_cp_envs[ env ] = component.Component( EnvViewer( le_appcode_provider = lambda: self.appcode, le_aera_provider = lambda: self.aera, env = env, resolvers = self ) )
      return self._d_cp_envs
   cp_envs = property( get_cp_envs )


@presentation.render_for( EnvsViewer )
def render(self, h, comp, *args):
   with h.div( class_ = 'envs_viewer %s' % ( self.aera ) ): 
      if not self.appcode:
         h << h.div( u'Veuillez selectionner un code application', class_ = 'appcodes message' )
      if not self.aera:
         h << h.div( u'Veuillez selectionner une zone', class_ = 'aeras message' )
      else:
         with self.cloudmap_resolver:
            d_order = self.env_resolver.order_for_envs.copy()
            for env, cp_env in sorted( self.cp_envs.items(), key = lambda e: d_order[ e[ 0 ] ], reverse = False ):
               with h.td():
                  h << h.div( component.Component( KnownDiv( cp_env ) ), class_ = 'envs_viewer_struct aera %s %s' %  ( self.aera, env ) )
                  h << h.div( h.div, class_ = 'envs_viewer_struct spacer' )

   return h.root
