# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers
from i_controllers                              import IAppcodeGetters, IEnvGetters
from counter_servers				import CounterServers

# cache de component
from i_cache_components                         import ICacheComponents


###########################
# Vision des zones
###########################
class MenuControlEnv( ICloudMgrResolvers, IAppcodeGetters, IEnvGetters, ICacheComponents ):

   def __init__( self, appcode = '', le_appcode_provider = None, env = '', le_env_provider = None, resolvers = None, cache_components = None ):
      ICloudMgrResolvers.__init__( self, resolvers )
      IAppcodeGetters.__init__( self, appcode = appcode, le_appcode_provider = le_appcode_provider )
      IEnvGetters.__init__( self, env = env, le_env_provider = le_env_provider )
      ICacheComponents.__init__( self, cache_components = cache_components )

      self._cp_counter_by_appcode_by_env = component.Component( CounterServers( le_appcode_provider = lambda: self.appcode, le_env_provider = lambda: self.env, resolvers = self, cache_components = self ) )
      self._cp_counter_by_env = component.Component( CounterServers( le_env_provider = lambda: self.env, resolvers = self, cache_components = self ) )


@presentation.render_for( MenuControlEnv )
def render(self, h, comp, *args):
   with self.cloudmap_resolver:
      with h.div( class_='menu_control_env %s' % ( self.env ) ):
        h << h.div( '%s ' % ( self.env_resolver.get_env_desc( self.env ) ), class_ = 'description' )
        h << h.div( component.Component( KnownDiv( self._cp_counter_by_appcode_by_env ) ), class_ = 'counter_appcomps_struct' )
        h << h.div( ' / ', class_ = 'counter_appcomps_struct separator' )
        h << h.div( component.Component( KnownDiv( self._cp_counter_by_env ) ), class_ = 'counter_appcomps_struct' )
   return h.root

@presentation.render_for( MenuControlEnv, model = '*' )
def render(self, h, comp, *args):
   with self.cloudmap_resolver:
      with h.div( class_='menu_control_env %s' % ( self.env ) ):
        h << h.div( 'Total ', class_ = 'description' )
        h << h.div( component.Component( KnownDiv( self._cp_counter_by_appcode_by_env ) ), class_ = 'counter_appcomps_struct' )
        h << h.div( ' / ', class_ = 'counter_appcomps_struct separator' )
        h << h.div( component.Component( KnownDiv( self._cp_counter_by_env ) ), class_ = 'counter_appcomps_struct' )
   return h.root
