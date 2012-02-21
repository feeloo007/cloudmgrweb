# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from aera_viewer				import AeraViewer
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from cloudmgrlib.m_cmgr_cloudmap_resolver       import with_cloudmap_resolver
import i_getter

from i_dom_tree					import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider, cached_component_for_dom

from pprint					import pprint


###########################
# Vision des zones
###########################
@i_getter.define_getter( 'appcode' )
class AerasViewer( 
         ICloudMgrResolvers, 
         IDomTree,
         IDynamicComponentProvider,
      ):

   def __init__( 
          self, 
          resolvers 		= None, 
          dom_storage 		= None, 
          dom_father 		= None, 
          l_static_init_params 	= [],
          *args,
          **kwargs
       ):

      ICloudMgrResolvers.__init__( 
         self, 
         resolvers 
      )

      IDynamicComponentProvider.__init__(
         self,
      )

      IDomTree.__init__(
         self,
         dom_storage 		= dom_storage,
         dom_father 		= dom_father,
         l_static_init_params 	= l_static_init_params,
         **kwargs
      )

      self.__d_all_le_cp_aeras_viewer = {}

   @with_cloudmap_resolver()
   def get_all_cp_aeras_viewer(
          self,
          *args,
          **kwargs
      ):

      d_all_cp_aeras_viewer = {}

      for aera in self.aera_resolver.all_aeras:

         if not self.__d_all_le_cp_aeras_viewer.has_key( aera ):

            @cached_component_for_dom(
               self,
               object_class         	= AeraViewer,
               l_static_init_params 	= [ 'aera' ],
               **{ 
                     'appcode'		: self.appcode,
                     'aera'		: aera 		
                 }
            )
            @with_cloudmap_resolver( self ) 
            def create_cp_aera(
                   *args,
                   **kwargs
                ):

               return AeraViewer( 
                         resolvers	= self, 
                         dom_storage 	= self,
                         dom_father  	= self,
                         *args,
                         **kwargs
                  ) 

            self.__d_all_le_cp_aeras_viewer[ aera ] = create_cp_aera

         d_all_cp_aeras_viewer[ aera ] = self.__d_all_le_cp_aeras_viewer[ aera ]()

      return d_all_cp_aeras_viewer

   all_cp_aeras_viewer = property( get_all_cp_aeras_viewer )


@presentation.render_for( AerasViewer )
@with_cloudmap_resolver()
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

   # définition de la fonction à appeler
   # pour l'évènement LOCAL_REFRESH_ON_APPCODE_SELECTED
   def update_on_LOCAL_REFRESH_ON_APPCODE_SELECTED( **kwargs ):
      assert( kwargs.has_key( 'appcode' ) ), u'appcode doit exister %s.%s' % ( 
                                                __name__,
                                                update_on_LOCAL_REFRESH_ON_APPCODE_SELECTED
                                             )
      self.appcode = kwargs[ 'appcode' ]

   # Ajout du selecteur d'évènements associés à la fonction
   # de mise à jour
   self.add_event_for_knowndiv(
      'LOCAL_REFRESH_ON_APPCODE_SELECTED',
      self,
      le_callback_update 	= update_on_LOCAL_REFRESH_ON_APPCODE_SELECTED,
      appcode 			= '*',
   )



   with h.div( 
           class_ = 'aeras_viewer' 
        ):

      if not self.appcode:

         h << h.div( 
                 u'Veuillez selectionner un code application', 
                 class_ = 'appcodes message' 
              )
      else:

         d_order = self.aera_resolver.order_for_aeras.copy()

         for aera, cp_aera_viewer in sorted( 
                                        self.all_cp_aeras_viewer.items(), 
                                        key 		= lambda e: d_order[ e[ 0 ] ], 
                                        reverse 	= False 
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
