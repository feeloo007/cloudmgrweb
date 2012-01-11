# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from i_controllers                              import IAppcodeGetters, IAeraGetters, IEnvGetters
from appcomp_viewer 				import AppCompViewer

###########################
# Vision des zones
###########################
class AppCompsViewer( ICloudMgrResolvers, IAppcodeGetters, IAeraGetters, IEnvGetters ):

   def __init__( self, appcode = '', le_appcode_provider = None, aera = '', le_aera_provider = None, env = '', le_env_provider = None, resolvers = None ):
      ICloudMgrResolvers.__init__( self, resolvers )
      IAppcodeGetters.__init__( self, appcode = appcode, le_appcode_provider = le_appcode_provider )
      IAeraGetters.__init__( self, aera = aera, le_aera_provider= le_aera_provider)
      IEnvGetters.__init__( self, env = env, le_env_provider= le_env_provider)

   def get_cp_appcomps( self ):
      with self.cloudmap_resolver:
         self._d_cp_appcomps = {}
         for appcomp in self.appcomp_resolver.get_all_appcomps_for_aera( self.aera ):
            self._d_cp_appcomps[ appcomp ] = component.Component( AppCompViewer( le_appcode_provider = lambda: self.appcode, le_aera_provider = lambda: self.aera, le_env_provider = lambda: self.env, appcomp = appcomp, resolvers = self ) )
      return self._d_cp_appcomps
   cp_appcomps = property( get_cp_appcomps )


@presentation.render_for( AppCompsViewer )
def render(self, h, comp, *args):
   
   with h.div( class_ = 'appcomps_viewer' ):
      if not self.appcode:
         h << h.div( u'Veuillez selectionner un code application', class_ = 'appcodes message' )
      if not self.aera:
         h << h.div( u'Veuillez selectionner une zone', class_ = 'aeras message' )
      if not self.env:
         h << h.div( u'Veuillez selectionner un environnement', class_ = 'envs message' )
      else:
         with self.cloudmap_resolver:
            d_order = self.appcomp_resolver.order_for_appcomps.copy()
            for appcomp, cp_appcomp in sorted( self.cp_appcomps.items(), key = lambda e: d_order[ e[ 0 ] ], reverse = False ):
               h << h.div( component.Component( KnownDiv( cp_appcomp ) ), class_ = 'appcomps_viewer_struct %s' % appcomp )
               h << h.div( h.div, class_ = 'appcomps_viewer_struct spacer' )

   return h.root
