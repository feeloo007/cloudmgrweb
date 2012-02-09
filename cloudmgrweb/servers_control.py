# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component, ajax
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from i_controllers                              import IAppcodeGetters, IAeraGetters, IEnvGetters, IAppCompGetters
from cloudmgrlib.m_cmgr_manage_virtual_stack    import create_next_dhcp_file_for, create_vm
from create_server_form				import CreateServerTask
from servers_viewer				import ServersViewer

from i_dom_tree                                 import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider

from pprint					import pprint


###########################
# Vision des zones
###########################
class ServersControl( 
         ICloudMgrResolvers, 
         IAppcodeGetters, 
         IAeraGetters, 
         IEnvGetters, 
         IAppCompGetters, 
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
                         le_appcomp_provider = le_appcomp_provider 
                      )

      IDomTree.__init__(
         self,
         dom_storage = dom_storage,
         dom_father = dom_father
      )

      IDynamicComponentProvider.__init__(
                                   self
                                )


      def create_cp_create_server_task():
         return component.Component( 
                   CreateServerTask( 
                      le_appcode_provider = lambda: self.appcode, 
                      le_aera_provider = lambda: self.aera, 
                      le_env_provider = lambda: self.env, 
                      le_appcomp_provider = lambda: self.appcomp, 
                      resolvers = self, 
                      dom_storage = self,
                      dom_father = self,
                   ),
                )

      self.create_dynamic_component(
         'cp_create_server_task',
         create_cp_create_server_task
      )


      def create_cp_servers_viewer():

         with self.cloudmap_resolver as cloudmap_resolver:

            return component.Component(
                             ServersViewer(
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
         'cp_servers_viewer',
         create_cp_servers_viewer
      )

@presentation.render_for( ServersControl )
def render(
       self, 
       h, 
       comp, 
       *args
    ):

   with self.cloudmap_resolver:

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
