# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers
import i_getter
from appcomps_viewer				import AppCompsViewer

from i_dom_tree                                 import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider


###########################
# Vision des zones
###########################
@i_getter.define_getter( 'appcode' )
@i_getter.define_getter( 'aera' )
@i_getter.define_getter( 'env' )
class EnvViewer( 
         ICloudMgrResolvers, 
         IDomTree,
         IDynamicComponentProvider,
      ):

   def __init__( 
          self, 
          resolvers 	= None, 
          dom_storage 	= None,
          dom_father 	= None,
          *args,
          **kwargs
       ):

      ICloudMgrResolvers.__init__( 
                            self, 
                            resolvers 
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
                          appcode 	= lambda: self.appcode, 
                          aera 		= lambda: self.aera, 
                          env 		= lambda: self.env, 
                          resolvers 	= self, 
                          dom_storage 	= self,
                          dom_father 	= self,
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
      self.reset_in_dom(
              comp
      )

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
