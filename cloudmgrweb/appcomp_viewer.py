# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers
from i_appcode_getter                           import IAppcodeGetter
from i_aera_getter                              import IAeraGetter
from i_env_getter                               import IEnvGetter
from i_appcomp_getter                           import IAppCompGetter
from servers_control				import ServersControl

from i_dom_tree                                 import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider


###########################
# Vision des zones
###########################
class AppCompViewer( 
         ICloudMgrResolvers, 
         IAppcodeGetter, 
         IAeraGetter,
         IEnvGetter, 
         IAppCompGetter, 
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
       ):

      ICloudMgrResolvers.__init__( 
         self, 
         resolvers 
      )

      IAppcodeGetter.__init__( 
         self, 
         appcode = appcode, 
         le_appcode_provider = le_appcode_provider 
      )

      IAeraGetter.__init__( 
         self, 
         aera = aera, 
         le_aera_provider = le_aera_provider 
      )

      IEnvGetter.__init__( 
         self, 
         env = env, 
         le_env_provider = le_env_provider 
      )

      IAppCompGetter.__init__( 
         self, 
         appcomp = appcomp, 
         le_appcomp_provider = None 
      )

      IDomTree.__init__(
         self,
         dom_storage = dom_storage,
         dom_father = dom_father
      )

      IDynamicComponentProvider.__init__(
         self
      )

      def create_cp_servers_control():
         return component.Component( 
                             ServersControl( 
                                le_appcode_provider = lambda: self.appcode, 
                                le_aera_provider = lambda: self.aera, 
                                le_env_provider = lambda: self.env, 
                                appcomp = appcomp, 
                                resolvers = self, 
                                dom_storage = self,
                                dom_father = self, 
                             ) 
                          )

      self.create_dynamic_component(
         'cp_servers_control',
         create_cp_servers_control
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
      self.reset_in_dom(
              comp
      )

      # Initialisation locale des composants
      # utilisés
      self.create_cp_servers_control()

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
                       self.cp_servers_control 
                    ) 
                 ), 
                 class_ = 'appcomp %s %s %s' % ( self.aera, self.env, self.appcomp ) 
              )

   return h.root
