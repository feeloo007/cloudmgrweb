# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component, ajax
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from i_controllers                              import IAppcodeGetters, IAeraGetters, IEnvGetters, IAppCompGetters
from cloudmgrlib.m_cmgr_manage_virtual_stack    import create_next_dhcp_file_for, create_vm
from server_viewer				import ServerViewer
from create_server_form				import CreateServerForm
from create_server_form				import CreateServerTask

# cache de component
from i_cache_components                         import ICacheComponents

###########################
# Vision des zones
###########################
class ServersViewer( ICloudMgrResolvers, IAppcodeGetters, IAeraGetters, IEnvGetters, IAppCompGetters, ICacheComponents ):

   def __init__( self, appcode = '', le_appcode_provider = None, aera = '', le_aera_provider = None, env = '', le_env_provider = None, appcomp = '', le_appcomp_provider = None, resolvers = None, cache_components = None ):
      ICloudMgrResolvers.__init__( self, resolvers )
      IAppcodeGetters.__init__( self, appcode = appcode, le_appcode_provider = le_appcode_provider )
      IAeraGetters.__init__( self, aera = aera, le_aera_provider = le_aera_provider)
      IEnvGetters.__init__( self, env = env, le_env_provider = le_env_provider)
      IAppCompGetters.__init__( self, appcomp = appcomp, le_appcomp_provider = le_appcomp_provider )
      ICacheComponents.__init__( self, cache_components = cache_components )

      self._cp_create_server_task = component.Component( CreateServerTask( le_appcode_provider = lambda: self.appcode, le_aera_provider = lambda: self.aera, le_env_provider = lambda: self.env, le_appcomp_provider = lambda: self.appcomp, resolvers = self, cache_components = self ) )

   def get_cp_servers( self ):
      with self.cloudmap_resolver as cloudmap_resolver:
         self._d_cp_servers = {}
         try:
             for num_component, d_component_status in cloudmap_resolver.cloudmap[ self.aera ][ self.appcode ][ self.env ][ self.appcomp ].items():
                self._d_cp_servers[ num_component ] = component.Component( ServerViewer( le_appcode_provider = lambda: self.appcode, le_aera_provider = lambda: self.aera, le_env_provider = lambda: self.env, le_appcomp_provider = lambda: self.appcomp, num_component = num_component, d_component_status = d_component_status, resolvers = self, cache_components = self ) )
         except Exception, e:
            pass
      return self._d_cp_servers   
   cp_servers = property( get_cp_servers )


@presentation.render_for( ServersViewer )
def render(self, h, comp, *args):
   self.uid = 'ServersViewer %s %s %s %s' % ( self.appcode, self.aera, self.env, self.appcomp )
   self.set_knowndiv_for( 'REFRESH_ON_CREATION_SERVER_DEMAND', self, appcode = self.appcode, aera = self.aera, env = self.env, appcomp = self.appcomp )

   with h.div( class_ = 'servers_viewer %s %s %s' % ( self.aera, self.env, self.appcomp ) ):

      if not self.appcode:
         h << h.div( u'Veuillez selectionner un code application', class_ = 'appcodes message' )
      if not self.aera:
         h << h.div( u'Veuillez selectionner une zone', class_ = 'aeras message' )
      if not self.env:
         h << h.div( u'Veuillez selectionner un environnement', class_ = 'envs message' )
      if not self.appcomp:
         h << h.div( u'Veuillez selectionner un composant applicatif', class_ = 'appcomps message' )
      else:
         with self.cloudmap_resolver as cloudmap_resolver:
            colspan = 4
            i = 0
            h << h.div( component.Component( KnownDiv( self._cp_create_server_task ) ), class_ = 'servers_viewer_struct create_server_task_struct %s %s %s' % ( self.aera, self.env, self.appcomp ) )
            h << h.div( h.div, class_ = 'servers_viewer_struct create_server_task_struct spacer' )
            div_block = None
            with h.div( '', class_ = 'servers_viewer_struct servers %s %s %s' % ( self.aera, self.env, self.appcomp ) ):
               with h.div( '', class_ = 'servers_viewer_struct scroll %s %s %s' % ( self.aera, self.env, self.appcomp ) ):
                  with h.div( '', class_ = 'servers_viewer_struct blocks' ):
                     for server, cp_server in sorted( self.cp_servers.items(), key = lambda e: e[ 0 ], reverse = False ):
                        if i % colspan == 0: 
                           div_block = h.div( '', class_ = 'servers_viewer_struct block %s %s %s' % ( self.aera, self.env, self.appcomp ) )
                           h << div_block
                        div_block.append( h.div( component.Component( KnownDiv( cp_server ) ), class_ = 'servers_viewer_struct component %s %s %s %s' % ( self.aera, self.env, self.appcomp, server  ) ) )
                        i = i + 1
   return h.root
