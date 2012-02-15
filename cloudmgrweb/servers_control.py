# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component, ajax
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from cloudmgrlib.m_cmgr_cloudmap_resolver       import with_cloudmap_resolver, with_cloudmap_resolver_for_render
import i_getter
from cloudmgrlib.m_cmgr_manage_virtual_stack    import create_next_dhcp_file_for, create_vm
from create_server_form				import CreateServerTask
from servers_viewer				import ServersViewer

from i_dom_tree                                 import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider

from pprint					import pprint


###########################
# Vision des zones
###########################
@i_getter.define_getter( 'appcode' )
@i_getter.define_getter( 'aera' )
@i_getter.define_getter( 'env' )
@i_getter.define_getter( 'appcomp' )
class ServersControl( 
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


      @with_cloudmap_resolver( self )
      def create_cp_create_server_task(
             *args,
             **kwargs
          ):
         return component.Component( 
                   CreateServerTask( 
                      appcode 		= lambda: self.appcode, 
                      aera 		= lambda: self.aera, 
                      env 		= lambda: self.env, 
                      appcomp 		= lambda: self.appcomp, 
                      resolvers 	= self, 
                      dom_storage 	= self,
                      dom_father 	= self,
                   ),
                )

      self.create_dynamic_component(
         'cp_create_server_task',
         create_cp_create_server_task
      )


      @with_cloudmap_resolver( self )
      def create_cp_servers_viewer(
             *args,
             **kwargs 
          ):

         return component.Component(
                   ServersViewer(
                      appcode 		= lambda: self.appcode,
                      aera 		= lambda: self.aera,
                      env 		= lambda: self.env,
                      appcomp 		= lambda: self.appcomp,
                      resolvers 	= self,
                      dom_storage 	= self,
                      dom_father 	= self,
                   )
                )


      self.create_dynamic_component(
         'cp_servers_viewer',
         create_cp_servers_viewer
      )

@presentation.render_for( ServersControl )
@with_cloudmap_resolver_for_render
def render(
       self, 
       h, 
       comp, 
       *args,
       **kwargs
    ):

   self.reset_in_dom(
           comp
   )

   with h.div( 
           class_ = 'servers_control %s %s %s' % ( self.aera, self.env, self.appcomp ) ):

      if not self.appcode:

         h << h.div( 
                 u'Veuillez selectionner un code application', 
                 class_ = 'appcodes message' 
              )

      elif not self.aera:

         h << h.div( 
                u'Veuillez selectionner une zone', 
                class_ = 'aeras message' 
              )

      elif not self.env:

         h << h.div( 
                 u'Veuillez selectionner un environnement', 
                 class_ = 'envs message' 
              )

      elif not self.appcomp:

         h << h.div( 
                 u'Veuillez selectionner un composant applicatif', 
                 class_ = 'appcomps message' 
              )

      else:

            self.create_cp_create_server_task()
            self.create_cp_servers_viewer()

            h << h.div( 
                    component.Component( 
                       KnownDiv( 
                          self.cp_create_server_task 
                       ) 
                    ), 
                    class_ = 'servers_control_struct create_server_task_struct %s %s %s' % ( self.aera, self.env, self.appcomp ) 
                 )

            h << h.div( 
                    h.div, 
                    class_ = 'servers_control_struct create_server_task_struct spacer' 
                 )

            h << h.div(
                    component.Component(
                       KnownDiv(
                          self.cp_servers_viewer
                       )
                    ),
                    class_ = 'servers_control_struct'
                 )

   return h.root
