# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers
from envs_viewer				import EnvsViewer
from i_controllers                              import IAppcodeGetters, IAeraGetters

from i_dom_tree                                 import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider


###########################
# Vision des zones
###########################
class AeraViewer( 
         ICloudMgrResolvers, 
         IAppcodeGetters, 
         IAeraGetters, 
         IDomTree,
         IDynamicComponentProvider, 
      ):

   def __init__( 
           self, aera = '', 
           le_aera_provider = None, 
           appcode = '', 
           le_appcode_provider = None, 
           resolvers = None, 
           dom_storage = None,
           dom_father = None,
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

      IDomTree.__init__(
                  self,
                  dom_storage = dom_storage,
                  dom_father = dom_father,
               )

      IDynamicComponentProvider.__init__(
                                   self,
                                )

      def create_cp_envs_viewer():
         return component.Component( 
                   EnvsViewer( 
                      le_appcode_provider = lambda: self.appcode, 
                      le_aera_provider = lambda: self.aera, 
                      resolvers = self, 
                      dom_storage = self,
                      dom_father = self,
                   ) 
                )


      self.create_dynamic_component(
         'cp_envs_viewer',
         create_cp_envs_viewer
      )


@presentation.render_for( AeraViewer )
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
      self.create_cp_envs_viewer()

      with h.div( 
              class_='aera_viewer %s' % ( self.aera )
           ):

         h << h.div( 
                 self.aera_resolver.get_aera_desc( self.aera ), 
                 class_ = 'description' 
              )

         h << h.div( 
                 component.Component( 
                    KnownDiv( 
                       self.cp_envs_viewer
                    ) 
                 ), 
                 class_ = 'aera %s' % ( self.aera ) 
            )

   return h.root
