# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers
from i_controllers                              import IAppcodeGetters, IAeraGetters, IEnvGetters, IAppCompGetters

# cache de component
from i_cache_components                         import ICacheComponents


###########################
# Vision des zones
###########################
class ServerViewer( ICloudMgrResolvers, IAppcodeGetters, IAeraGetters, IEnvGetters, IAppCompGetters, ICacheComponents ):

   def __init__( self, appcode = '', le_appcode_provider = None, aera = '', le_aera_provider = None, env = '', le_env_provider = None, appcomp = '', le_appcomp_provider = None, num_component = '', d_component_status = {} , resolvers = None, cache_components = None ):

      ICloudMgrResolvers.__init__( self, resolvers )
      IAppcodeGetters.__init__( self, appcode = appcode, le_appcode_provider = le_appcode_provider )
      IAeraGetters.__init__( self, aera = aera, le_aera_provider = le_aera_provider )
      IEnvGetters.__init__( self, env = env, le_env_provider = le_env_provider )
      IAppCompGetters.__init__( self, appcomp = appcomp, le_appcomp_provider = le_appcomp_provider )
      ICacheComponents.__init__( self, cache_components = cache_components )

      self._num_component 	= num_component
      self._d_component_status 	= d_component_status
      self._servername 		= '%s-%s-%s' % ( self.appcomp, self.num_component, self.aera )

   def get_num_component( self ):
      return self._num_component
   num_component = property( get_num_component )

   def get_d_component_status( self ):
      return self._d_component_status
   d_component_status = property( get_d_component_status )

   def get_servername( self ):
      return self._servername
   servername = property( get_servername )


@presentation.render_for( ServerViewer )
def render(self, h, comp, *args):
   with self.cloudmap_resolver as cloudmap_resolver:
      with h.div( class_='component %s %s %s %s' % ( self.aera, self.env, self.appcomp, self.servername ) ):
         with h.table():
            with h.tr():
               with h.td(): 
                  with h.div( class_ = 'description' ):
                     h << '%s' % ( self.servername )
            with h.tr():
               with h.td(): 
                  with h.div():
                     pass
   return h.root
