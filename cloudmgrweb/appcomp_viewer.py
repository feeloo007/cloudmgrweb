# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers
from i_controllers                              import IAppcodeGetters, IAeraGetters, IEnvGetters, IAppCompGetters
from servers_viewer				import ServersViewer

# cache de component
from i_cache_components                         import ICacheComponents

from i_dom_tree                                 import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider


###########################
# Vision des zones
###########################
class AppCompViewer( 
         ICloudMgrResolvers, 
         IAppcodeGetters, 
         IAeraGetters,
         IEnvGetters, 
         IAppCompGetters, 
         ICacheComponents,
         IDomTree,
         IDynamicComponentProvider
      ):

   def __init__( 
          self, appcode = '', 
          le_appcode_provider = None, 
          aera = '', 
          le_aera_provider = None, 
          env = '', 
          le_env_provider = None, 
          appcomp = '', 
          le_appcomp_provider = None, 
          resolvers = None, 
          dom_storage = None,
          dom_father = None,
          cache_components = None
       ):

      ICloudMgrResolvers.__init__( 
         self, 
         resolvers 
      )

      IAppcodeGetters.__init__( 
         self, 
         appcode = appcode, 
         le_appcode_provider = le_appcode_provider 
      )

      IAeraGetters.__init__( 
         self, 
         aera = aera, 
         le_aera_provider = le_aera_provider 
      )

      IEnvGetters.__init__( 
         self, 
         env = env, 
         le_env_provider = le_env_provider 
      )

      IAppCompGetters.__init__( 
         self, 
         appcomp = appcomp, 
         le_appcomp_provider = None 
      )

      ICacheComponents.__init__( 
         self, 
         cache_components = cache_components 
      )

      IDomTree.__init__(
         self,
         dom_storage = dom_storage,
         dom_father = dom_father
      )

      IDynamicComponentProvider.__init__(
         self
      )

      def create_cp_servers_viewer():
         return component.Component( 
                             ServersViewer( 
                                le_appcode_provider = lambda: self.appcode, 
                                le_aera_provider = lambda: self.aera, 
                                le_env_provider = lambda: self.env, 
                                appcomp = appcomp, 
                                resolvers = self, 
                                dom_storage = self,
                                dom_father = self, 
                                cache_components = self 
                             ) 
                          )

      self.create_dynamic_component(
         'cp_servers_viewer',
         create_cp_servers_viewer
      )

@presentation.render_for( AppCompViewer )
def render(
       self, 
       h, 
       comp, 
       *args
    ):

   with self.cloudmap_resolver:

      # Suppression des précédents fils
      # dans le modèle DOM
      self.delete_dom_childs()

      # Initialisation locale des composants
      # utilisés
      self.create_cp_servers_viewer()

      with h.div( 
              class_='appcomp_viewer %s %s %s' % ( self.aera, self.env, self.appcomp ) 
           ):

         h << h.div( 
                 self.appcomp_resolver.get_appcomp_desc( self.appcomp ), 
                 class_ = 'description' 
         )

         h << h.div( 
                 component.Component( 
                    KnownDiv( 
                       self.cp_servers_viewer 
                    ) 
                 ), 
                 class_ = 'appcomp %s %s %s' % ( self.aera, self.env, self.appcomp ) 
              )

   return h.root
