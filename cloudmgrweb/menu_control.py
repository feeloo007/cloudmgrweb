# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import component, presentation
from appcode_selector				import AppcodeSelector
from menu_control_envs	 			import MenuControlEnvs
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers

# Interaction comet
from i_comet					import ICloudMgrComet
from nagare					import ajax

# cache de component
from i_cache_components				import ICacheComponents, FormRefreshOnComet

# Mise en place d'un DOM pour la gestion comet
from i_dom                                      import IDom

class MenuControl( ICloudMgrResolvers, ICloudMgrComet, ICacheComponents, IDom ):
   def __init__( self, dom_father = None, dom_element_name = '' ):
      ICloudMgrResolvers.__init__( self )

      # Interaction comet
      ICloudMgrComet.__init__( self )

      # cache de components
      ICacheComponents.__init__( self, cache_components = None )

      # Mise en place d'un DOM pour la gestion comet
      IDom.__init__( self, dom_father = dom_father, dom_element_name = dom_element_name  )

      with self.cloudmap_resolver:
         self._cp_appcode_selector 	= component.Component( AppcodeSelector() )
         self._cp_menu_control_envs 	= component.Component( MenuControlEnvs( le_appcode_provider = lambda: self.cp_appcode_selector.o.appcode, resolvers = self, cache_components = self, dom_father = self, dom_element_name = '%s' % MenuControlEnvs.__name__ ) )

   def get_cp_appcode_selector( self ):
      return self._cp_appcode_selector
   
   cp_appcode_selector = property( get_cp_appcode_selector )

   def get_cp_menu_control_envs( self ):
      return self._cp_menu_control_envs

   cp_menu_control_envs = property( get_cp_menu_control_envs )

@presentation.render_for(MenuControl)
def render(self, h, *args):

   cp_div_appcode_selector	= component.Component( KnownDiv( self._cp_appcode_selector ) )
   cp_div_menu_control_envs	= component.Component( KnownDiv( self._cp_menu_control_envs ) )

   # Interaction comet
   with self.cloudmap_resolver:

      with h.div( class_ = 'menu_control' ):
         h << h.div( cp_div_appcode_selector, class_ = 'menu_control_struct APPCODE' )
         h << h.div( '', class_ = 'menu_control_struct spacer' )
         h << h.div( cp_div_menu_control_envs, class_ = 'menu_control_struct ENVS' )

   return h.root
