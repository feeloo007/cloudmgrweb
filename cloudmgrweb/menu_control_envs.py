# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from menu_control_env				import MenuControlEnv
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from cloudmgrlib.m_cmgr_cloudmap_resolver       import with_cloudmap_resolver
import i_getter

from i_dom_tree					import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider

from pprint					import pprint

###########################
# Vision des zones
###########################
@i_getter.define_getter( 'appcode' )
class MenuControlEnvs( 
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

      IDynamicComponentProvider.__init__( 
         self 
      )

      IDomTree.__init__( 
         self, 
         dom_storage = dom_storage, 
         dom_father = dom_father 
      )

      # Définition des composants dynamiques
      # Filtre uniquement sur le code application
      @with_cloudmap_resolver( self )
      def create_cp_menu_all_envs(
             *args,
             **kwargs
          ):
         return component.Component(
                   MenuControlEnv( 
                      env 		= '*', 
                      appcode 		= lambda: self.appcode, 
                      resolvers 	= self, 
                      dom_storage 	= self,
                      dom_father 	= self, 
                   ),
                   model = '*' 
                ) 

      self.create_dynamic_component(
         'cp_menu_all_envs',
         create_cp_menu_all_envs
      )

      # filtre environnement par environnnement
      @with_cloudmap_resolver( self )
      def create_d_cp_menu_by_envs(
             *args,
             **kwargs
         ):
         d_cp_menu_by_envs = {}
         for env in self.env_resolver.all_envs:
            d_cp_menu_by_envs[ env ] = component.Component( 
                                          MenuControlEnv( 
                                             env 		= env, 
                                             appcode 		= lambda: self.appcode, 
                                             resolvers 		= self, 
                                             dom_storage 	= self,
                                             dom_father 	= self, 
                                          ) 
                                       ) 
         return d_cp_menu_by_envs

      self.create_dynamic_component(
         'd_cp_menu_by_envs',
         create_d_cp_menu_by_envs
      )


@presentation.render_for( MenuControlEnvs )
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
      le_callback_update     	= update_on_LOCAL_REFRESH_ON_APPCODE_SELECTED,
      appcode 			= '*',
   )

   # Initialisation locale des composants
   # utilisés
   self.create_cp_menu_all_envs()
   self.create_d_cp_menu_by_envs()

   with h.div( 
           class_ = 'menu_control_envs' 
        ): 

      d_order = self.env_resolver.order_for_envs.copy()

      for env, cp_menu_by_env in sorted( 
                                    self.d_cp_menu_by_envs.items(), 
                                    key = lambda e: d_order[ e[ 0 ] ], 
                                    reverse = False 
                                 ):

         h << h.div( 
                 component.Component( 
                    KnownDiv( 
                      cp_menu_by_env 
                    ) 
                 ), 
                 class_ = 'menu_control_envs_struct %s' %  ( env ) 
              )

         h << h.div( 
                 h.div, 
                 class_ = 'menu_control_envs_struct spacer' 
              )

      h << h.div( 
              component.Component( 
                 KnownDiv( 
                    self.cp_menu_all_envs 
                 ) 
              ), 
              class_ = 'menu_control_envs_struct SUM' 
           )

      h << h.div( 
              h.div, 
              class_ = 'menu_control_envs_struct spacer' 
           )

   return h.root
