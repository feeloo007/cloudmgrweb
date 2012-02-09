# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
import i_getter

from appcomp_viewer 				import AppCompViewer

from i_dom_tree                                 import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider


###########################
# Vision des zones
###########################
@i_getter.define_getter( 'appcode' )
@i_getter.define_getter( 'aera' )
@i_getter.define_getter( 'env' )
class AppCompsViewer( 
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
                  dom_father = dom_father,
               )

      IDynamicComponentProvider.__init__(
                                   self
                                )


      def create_all_cp_appcomps_viewer():
         with self.cloudmap_resolver:
            d_all_cp_appcomps = {}
            for appcomp in self.appcomp_resolver.get_all_appcomps_for_aera( self.aera ):
               d_all_cp_appcomps[ appcomp ] = component.Component( 
                                                 AppCompViewer( 
                                                    appcode 	= lambda: self.appcode, 
                                                    aera 	= lambda: self.aera, 
                                                    env 	= lambda: self.env, 
                                                    appcomp 	= appcomp, 
                                                    resolvers 	= self, 
                                                    dom_storage = self,
                                                    dom_father 	= self,
                                                 ) 
                                              )
            return d_all_cp_appcomps

      self.create_dynamic_component(
         'all_cp_appcomps_viewer',
         create_all_cp_appcomps_viewer
      )
   

@presentation.render_for( AppCompsViewer )
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
              class_ = 'appcomps_viewer %s %s' % ( self.aera, self.env ) 
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

         elif not self.env:

            h << h.div( u'Veuillez selectionner un environnement', class_ = 'envs message' )

         else:

            self.create_all_cp_appcomps_viewer()

            d_order = self.appcomp_resolver.order_for_appcomps.copy()
            for appcomp, cp_appcomp_viewer in sorted( 
                                          self.all_cp_appcomps_viewer.items(), 
                                          key = lambda e: d_order[ e[ 0 ] ], 
                                          reverse = False 
                                       ):

               h << h.div( 
                       component.Component( 
                          KnownDiv( 
                             cp_appcomp_viewer
                          ) 
                       ), 
                       class_ = 'appcomps_viewer_struct appcomp %s %s %s' % ( self.aera, self.env, appcomp ) 
                    )
 
               h << h.div( 
                       h.div, 
                       class_ = 'appcomps_viewer_struct spacer' 
                    )
 
   return h.root
