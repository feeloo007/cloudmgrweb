# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from aera_viewer				import AeraViewer
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from i_controllers				import IAppcodeGetters

from i_dom_tree					import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider

from pprint					import pprint


###########################
# Vision des zones
###########################
class AerasViewer( 
         ICloudMgrResolvers, 
         IAppcodeGetters, 
         IDomTree,
         IDynamicComponentProvider,
      ):

   def __init__( 
          self, 
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
 
      IDynamicComponentProvider.__init__(
         self,
      )

      IDomTree.__init__(
         self,
         dom_storage 	= dom_storage,
         dom_father 	= dom_father,
      )


      # Définition des composants dynamiques
      # Menu de controle
      def create_all_cp_aeras_viewer():
         with self.cloudmap_resolver:
            d_all_cp_aeras_viewer = {}
            for aera in self.aera_resolver.all_aeras:
               d_all_cp_aeras_viewer[ aera ] = component.Component( 
                                                 AeraViewer( 
                                                    aera = aera, 
                                                    le_appcode_provider = lambda: self.appcode, 
                                                    resolvers = self, 
                                                    dom_storage = self,
                                                    dom_father = self,
                                                 ) 
                                              )
         return d_all_cp_aeras_viewer

      self.create_dynamic_component(
         'all_cp_aeras_viewer',
         create_all_cp_aeras_viewer
      )


@presentation.render_for( AerasViewer )
def render(self, h, comp, *args):

   with self.cloudmap_resolver:

      # Suppression des précédents fils
      # dans le modèle DOM
      self.reset_in_dom(
              comp
      )

      self.add_event_for_knowndiv(
         'LOCAL_REFRESH_ON_APPCODE_SELECTED',
         self,
         appcode = '*',
      )

      with h.div( 
              class_ = 'aeras_viewer' 
           ):

         if not self.appcode:

            h << h.div( 
                    u'Veuillez selectionner un code application', 
                    class_='appcodes message' 
                 )
         else:

            # Initialisation locale des composants
            # utilisés
            self.create_all_cp_aeras_viewer()

            d_order = self.aera_resolver.order_for_aeras.copy()

            for aera, cp_aera_viewer in sorted( 
                                           self.all_cp_aeras_viewer.items(), 
                                           key = lambda e: d_order[ e[ 0 ] ], 
                                           reverse = False 
                                        ):

               h << h.div( 
                       component.Component( 
                          KnownDiv( 
                             cp_aera_viewer
                          ) 
                       ), 
                       class_ = 'aeras_viewer_struct %s' % aera 
                    )

               h << h.div(  
                       h.div, 
                       class_ = 'aeras_viewer_struct spacer' 
               )

   return h.root
