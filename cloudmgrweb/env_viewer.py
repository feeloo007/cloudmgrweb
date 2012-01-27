# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers
from i_controllers                              import IAppcodeGetters, IAeraGetters, IEnvGetters
from appcomps_viewer				import AppCompsViewer

# cache de component
from i_cache_components                         import ICacheComponents

from i_dom_tree                                 import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider


###########################
# Vision des zones
###########################
class EnvViewer( 
         ICloudMgrResolvers, 
         IAppcodeGetters, 
         IAeraGetters, 
         IEnvGetters, 
         ICacheComponents,
         IDomTree,
         IDynamicComponentProvider,
      ):

   def __init__( 
          self, 
          appcode = '', 
          le_appcode_provider = None, 
          aera = '', 
          le_aera_provider = None, 
          env = '', 
          le_env_provider = None, 
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

      def create_cp_appcomps_viewer():
         with self.cloudmap_resolver:
             return component.Component( 
                       AppCompsViewer( 
                          le_appcode_provider = lambda: self.appcode, 
                          le_aera_provider = lambda: self.aera, 
                          le_env_provider = lambda: self.env, 
                          resolvers = self, 
                          dom_storage = self,
                          dom_father = self,
                          cache_components = self 
                       ) 
                    )


      self.create_dynamic_component(
         'cp_appcomps_viewer',
         create_cp_appcomps_viewer
      )

@presentation.render_for( EnvViewer )
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
      self.create_cp_appcomps_viewer()

      with h.div( 
              class_='env_viewer %s %s' % ( self.aera, self.env ) 
           ):

         h << h.div( 
                 self.env_resolver.get_env_desc( self.env ), 
                 class_ = 'description' 
              )

         h << h.div( 
                 component.Component( 
                    KnownDiv(  
                       self.cp_appcomps_viewer 
                    ) 
                 ), 
                 class_ = 'env %s %s' % ( self.aera, self.env ) 
              )

   return h.root
