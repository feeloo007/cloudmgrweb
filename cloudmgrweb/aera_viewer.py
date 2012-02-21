# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers
from cloudmgrlib.m_cmgr_cloudmap_resolver       import with_cloudmap_resolver, with_cloudmap_resolver_for_render
from envs_viewer				import EnvsViewer

import i_getter

from i_dom_tree                                 import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider


###########################
# Vision des zones
###########################
@i_getter.define_getter( 'appcode' )
@i_getter.define_getter( 'aera' )
class AeraViewer( 
         ICloudMgrResolvers, 
         IDomTree,
         IDynamicComponentProvider, 
      ):

   def __init__( 
           self, 
           resolvers 			= None, 
           dom_storage 			= None,
           dom_father 			= None,
           l_static_init_params   	= [],
           **kwargs
       ):

      ICloudMgrResolvers.__init__( 
                            self, 
                            resolvers 
                         )

      IDomTree.__init__(
                  self,
                  dom_storage 		= dom_storage,
                  dom_father 		= dom_father,
                  l_static_init_params 	= l_static_init_params,
                  **kwargs
               )

      IDynamicComponentProvider.__init__(
                                   self,
                                )

      @with_cloudmap_resolver( self )
      def create_cp_envs_viewer(
             *args,
             **kwargs
          ):
         return component.Component( 
                   EnvsViewer( 
                      appcode 		= lambda: self.appcode, 
                      aera 		= lambda: self.aera, 
                      resolvers 	= self, 
                      dom_storage 	= self,
                      dom_father 	= self,
                   ) 
                )


      self.create_dynamic_component(
         'cp_envs_viewer',
         create_cp_envs_viewer
      )


@presentation.render_for( AeraViewer )
@with_cloudmap_resolver_for_render
def render(
       self, 
       h, 
       comp, 
       *args,
       **kwargs
    ):

   # Suppression des précédents fils
   # dans le modèle DOM
   self.reset_in_dom(
           comp
   )

   # Initialisation locale des composants
   # utilisés
   self.create_cp_envs_viewer()

   with h.div( 
           class_ = 'aera_viewer %s' % ( self.aera )
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
