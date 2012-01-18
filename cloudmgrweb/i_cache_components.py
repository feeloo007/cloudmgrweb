# -*- coding: UTF-8 -*-
from __future__ 	import with_statement
from nagare		import presentation, var
from ajax_x_components  import XComponentsUpdates
from pprint		import pprint

class ICacheComponents( object ):

   def __init__( self, cache_components = None ):
      if not cache_components:
         self._cache_components = {}
      else:
         self._cache_components = cache_components.cache_components

   def get_cache_components( self ):
     return self._cache_components

   cache_components = property( get_cache_components )

   def set_knowndiv_for( self, event_name, cp_div, appcode = '*', aera = '*', env = '*', appcomp = '*' ):

      self.cache_components.setdefault(
         event_name,
         {}
      ).setdefault(
         appcode,
         {}
      ).setdefault(
         aera,
         {}
      ).setdefault(
         env,
         {}
      ).setdefault( 
          appcomp, 
          {}                                  
      ).setdefault( 
           cp_div.full_dom_element_name,
           lambda: cp_div.le_get_knowndiv()
      )


   def get_l_known_div_for_change( self, event_name, appcode = '*', aera = '*', env = '*', appcomp = '*' ):

      pprint( u'event_name: %s' % event_name )  
      pprint( u'appcode: %s' % appcode )  
      pprint( u'aera: %s' % aera )  
      pprint( u'env: %s' % env )  
      pprint( u'appcomp: %s' % appcomp )  

      pprint( self.cache_components )

      return [ le() for le in self.cache_components.get(
            event_name
         ).get(
           appcode
         ).get(
           aera
         ).get(
           env
         ).get( appcomp ).values()
      ]

class FormRefreshOnComet( ICacheComponents ):
   def __init__( self, cache_components = None ):
      ICacheComponents.__init__( self, cache_components = cache_components )

@presentation.render_for( FormRefreshOnComet )
def render(self, h, *args):

   v_event_name = var.Var()
   v_appcode 	= var.Var()
   v_aera 	= var.Var()
   v_env 	= var.Var()
   v_appcomp 	= var.Var()
   
   def fake():
      pass

   with h.form( id = 'refresh_on_comet_event' ):
         #h << h.input( type = 'submit', class_ = 'submit', style = 'display: none ;' ).action( fake )
         h << h.input( type = 'submit', class_ = 'submit', style = 'display: none ;' ).action( XComponentsUpdates( le_l_knowndiv = lambda: self.get_l_known_div_for_change( v_event_name(), appcode = v_appcode(), aera = v_aera(), env = v_env(), appcomp = v_appcomp() ), update_himself = True, action = lambda: fake() ) )
         h << h.input( type = 'hidden', class_ = 'event_name' ).action( v_event_name )
         h << h.input( type = 'hidden', class_ = 'appcode' ).action( v_appcode )
         h << h.input( type = 'hidden', class_ = 'aera' ).action( v_aera )
         h << h.input( type = 'hidden', class_ = 'env' ).action( v_env )
         h << h.input( type = 'hidden', class_ = 'appcomp' ).action( v_appcomp )

   return h.root
