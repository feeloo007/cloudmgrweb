# -*- coding: UTF-8 -*-
from __future__ 				import with_statement
from nagare					import presentation, var
from ajax_x_components  			import XComponentsUpdates
from pprint					import pprint
from cloudmgrlib.sequential_ops			import SequentialOps

class ICacheComponents( object ):

   def __init__( self, cache_components = None ):
      if not cache_components:
         self._cache_components = {}
      else:
         self._cache_components = cache_components.cache_components

   def get_cache_components( self ):
     return self._cache_components

   cache_components = property( get_cache_components )

   def set_knowndiv_for( self, event_name, cp_div, appcode = '-', aera = '-', env = '-', appcomp = '-' ):

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
      )[ cp_div.full_dom_element_name ] = lambda: cp_div.le_get_knowndiv()


   def get_l_known_div_for_change( self, event_name, appcode = '*', aera = '*', env = '*', appcomp = '*' ):

      def get_list_from_key( l, key ):
         l_result = []
         for e in l:
            result = []

            if e <> '*':
               result = e.get( key, [] )
            else:
               result = e.values()

            if type( result ) == dict:
               result = [ result ]

            l_result.extend( result )

            result = []
            result = e.get( '*', [] )

            if type( result ) == dict:
               result = [ result ]

            l_result.extend( result )

            result = []
            result = e.get( '-', [] )

            if type( result ) == dict:
               result = [ result ]

            l_result.extend( result )
            
         return l_result

      def print_struct( x ):
         pprint( x )
         print
         return x

      def to_l_le( l ):
         l_result = []
         for d in l:
            result = None
            result = d.values()
            if type( result ) == dict:
               result = [ result ]
            l_result.extend( result )
         return l_result

      def process_l_le( l ):
         return [ le() for le in l ]
         

      seq = SequentialOps( 
         [ self.cache_components ], 
         [ 
            lambda l, key = event_name: get_list_from_key( l, key ),
            lambda l, key = appcode: get_list_from_key( l, key ),
            lambda l, key = aera: get_list_from_key( l, key ),
            lambda l, key = env: get_list_from_key( l, key ),
            lambda l, key = appcomp: get_list_from_key( l, key ),
            to_l_le,
            process_l_le,
         ] 
      )

      return seq.process()



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
