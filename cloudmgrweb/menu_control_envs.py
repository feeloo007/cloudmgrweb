# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from menu_control_env				import MenuControlEnv
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from i_controllers                              import IAppcodeGetters


# cache de component
from i_cache_components                         import ICacheComponents

# Mise en place d'un DOM pour la gestion comet
from i_dom                                      import IDom

###########################
# Vision des zones
###########################
class MenuControlEnvs( ICloudMgrResolvers, IAppcodeGetters, ICacheComponents, IDom ):

   def __init__( self, appcode = '', le_appcode_provider = None, resolvers = None, cache_components = None, dom_father = None, dom_element_name = '' ):
      ICloudMgrResolvers.__init__( self, resolvers )
      IAppcodeGetters.__init__( self, appcode = appcode, le_appcode_provider = le_appcode_provider )
      ICacheComponents.__init__( self, cache_components = cache_components )

      # Mise en place d'un DOM pour la gestion comet
      IDom.__init__( self, dom_father = dom_father, dom_element_name = dom_element_name  )

      print self.full_dom_element_name

      # Filtre uniquement sur le code application
      self._cp_env_all_envs = component.Component( MenuControlEnv( le_appcode_provider = lambda: self.appcode, resolvers = self, cache_components = self ), model = '*' )

   def get_cp_envs( self ):
      with self.cloudmap_resolver:
         self._d_cp_envs = {}
         for env in self.env_resolver.all_envs:
            # Filtre sur le code applciation en l'environnement
            self._d_cp_envs[ env ] = component.Component( MenuControlEnv( env = env, le_appcode_provider = lambda: self.appcode, resolvers = self, cache_components = self ) )
      return self._d_cp_envs
   cp_envs = property( get_cp_envs )


@presentation.render_for( MenuControlEnvs )
def render(self, h, comp, *args):
   with h.div( class_ = 'menu_control_envs' ): 
      with self.cloudmap_resolver:
         d_order = self.env_resolver.order_for_envs.copy()
         for env, cp_env in sorted( self.cp_envs.items(), key = lambda e: d_order[ e[ 0 ] ], reverse = False ):
            h << h.div( component.Component( KnownDiv( cp_env ) ), class_ = 'menu_control_envs_struct %s' %  ( env ) )
            h << h.div( h.div, class_ = 'menu_control_envs_struct spacer' )
         h << h.div( component.Component( KnownDiv( self._cp_env_all_envs ) ), class_ = 'menu_control_envs_struct SUM' )
         h << h.div( h.div, class_ = 'menu_control_envs_struct spacer' )

   return h.root
