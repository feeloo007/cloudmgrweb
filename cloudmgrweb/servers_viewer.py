# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component, ajax
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from cloudmgrlib.m_cmgr_cloudmap_resolver       import with_cloudmap_resolver, with_cloudmap_resolver_for_render
import i_getter
from cloudmgrlib.m_cmgr_manage_virtual_stack    import create_next_dhcp_file_for, create_vm
from server_viewer				import ServerViewer

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
class ServersViewer( 
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
      def create_all_cp_servers_viewer(
             *args,
             **kwargs
          ):

         d_all_cp_servers_viewer = {}
         try:
            for num_component, d_component_status in kwargs[ 'with_cloudmap_resolver' ].cloudmap[ self.aera ][ self.appcode ][ self.env ][ self.appcomp ].items():
               d_all_cp_servers_viewer[ num_component ] = component.Component( 
                                                             ServerViewer( 
                                                                appcode 		= lambda: self.appcode, 
                                                                aera 			= lambda: self.aera, 
                                                                env 			= lambda: self.env, 
                                                                appcomp 		= lambda: self.appcomp, 
                                                                num_component 		= num_component, 
                                                                d_component_status 	= d_component_status, 
                                                                resolvers 		= self, 
                                                                dom_storage 		= self,
                                                                dom_father 		= self,
                                                             ) 
                                                          ) 
         except Exception, e:
            pass

         return d_all_cp_servers_viewer

      self.create_dynamic_component(
         'all_cp_servers_viewer',
         create_all_cp_servers_viewer
      )

@presentation.render_for( ServersViewer )
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
           class_ = 'servers_viewer %s %s %s' % ( self.aera, self.env, self.appcomp ) ):

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

            self.create_all_cp_servers_viewer()

            #self.set_knowndiv_for( 'REFRESH_ON_CREATION_SERVER_DEMAND', self, appcode = self.appcode, aera = self.aera, env = self.env, appcomp = self.appcomp )

            self.add_event_for_knowndiv( 
               'REFRESH_ON_CREATION_SERVER_DEMAND', 
               self, 
               appcode = self.appcode, 
               aera = self.aera, 
               env = self.env, 
               appcomp = self.appcomp
            )


            colspan = 4
            i = 0

            div_block = None

            with h.div( 
                    '', 
                    class_ = 'servers_viewer_struct servers %s %s %s' % ( self.aera, self.env, self.appcomp ) 
                 ):

               with h.div( 
                       '', 
                       class_ = 'servers_viewer_struct scroll %s %s %s' % ( self.aera, self.env, self.appcomp ) 
                    ):

                  with h.div( 
                          '', 
                          class_ = 'servers_viewer_struct blocks' 
                       ):

                     for server, cp_server_viewer in sorted( 
                                                        self.all_cp_servers_viewer.items(), 
                                                        key = lambda e: e[ 0 ], 
                                                        reverse = False 
                                                     ):

                        if i % colspan == 0: 

                           div_block = h.div( 
                                          '', 
                                          class_ = 'servers_viewer_struct block %s %s %s' % ( self.aera, self.env, self.appcomp ) 
                                       )
                           h << div_block

                        div_block.append( 
                           h.div( 
                              component.Component( 
                                 KnownDiv( 
                                    cp_server_viewer 
                                 ) 
                              ), 
                              class_ = 'servers_viewer_struct component %s %s %s %s' % ( self.aera, self.env, self.appcomp, server  ) 
                           ) 
                        )
                        i = i + 1

   return h.root
