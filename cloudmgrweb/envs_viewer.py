# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from env_viewer					import EnvViewer
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from i_appcode_getter                           import IAppcodeGetter
from i_aera_getter                              import IAeraGetter

from i_dom_tree                                 import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider


###########################
# Vision des zones
###########################
class EnvsViewer( 
         ICloudMgrResolvers, 
         IAppcodeGetter, 
         IAeraGetter, 
         IDomTree,
         IDynamicComponentProvider
      ):

   def __init__( 
          self, 
          appcode = '', 
          le_appcode_provider = None, 
          aera = '', 
          le_aera_provider = None, 
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
         le_aera_provider= le_aera_provider 
      )

      IDomTree.__init__(
         self,
         dom_father = dom_father,
         dom_storage = dom_storage,
      )

      IDynamicComponentProvider.__init__(
         self,
      )

      def create_all_cp_envs_viewer():
         with self.cloudmap_resolver:
            d_all_cp_envs = {}
            for env in self.env_resolver.all_envs:
               d_all_cp_envs[ env ] = component.Component( 
                                    EnvViewer( 
                                       le_appcode_provider = lambda: self.appcode, 
                                       le_aera_provider = lambda: self.aera, 
                                       env = env, 
                                       resolvers = self, 
                                       dom_storage = self,
                                       dom_father = self,
                                    ) 
                                 )
            return d_all_cp_envs

      self.create_dynamic_component(
         'all_cp_envs_viewer',
         create_all_cp_envs_viewer
      )


@presentation.render_for( EnvsViewer )
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


      with h.div( 
              class_ = 'envs_viewer %s' % ( self.aera ) 
           ):
 
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

         else:

            # Initialisation locale des composants
            # utilisés
            self.create_all_cp_envs_viewer()

            d_order = self.env_resolver.order_for_envs.copy()
            for env, cp_env_viewer in sorted( 
                                         self.all_cp_envs_viewer.items(), 
                                         key = lambda e: d_order[ e[ 0 ] ], 
                                        reverse = False
                                      ):

               h << h.div( 
                       component.Component( 
                          KnownDiv( 
                             cp_env_viewer 
                          )
                       ), 
                       class_ = 'envs_viewer_struct aera %s %s' %  ( self.aera, env )
               )

               h << h.div( 
                       h.div, 
                       class_ = 'envs_viewer_struct spacer'
                    )

   return h.root
