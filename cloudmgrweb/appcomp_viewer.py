# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers
import i_getter
from servers_control				import ServersControl

from i_dom_tree                                 import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider


###########################
# Vision des zones
###########################
@i_getter.define_getter( 'appcode' )
@i_getter.define_getter( 'aera' )
@i_getter.define_getter( 'env' )
@i_getter.define_getter( 'appcomp' )
class AppCompViewer( 
         ICloudMgrResolvers, 
         IDomTree,
         IDynamicComponentProvider
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

      def create_cp_servers_control():
         return component.Component( 
                             ServersControl( 
                                appcode 	= lambda: self.appcode, 
                                aera 		= lambda: self.aera, 
                                env 		= lambda: self.env, 
                                appcomp 	= lambda: self.appcomp, 
                                resolvers 	= self, 
                                dom_storage 	= self,
                                dom_father 	= self, 
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
