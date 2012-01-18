# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component, ajax
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from i_controllers                              import IAppcodeGetters, IAeraGetters, IEnvGetters, IAppCompGetters
from cloudmgrlib.sequential_ops			import SequentialOps

# cache de component
from i_cache_components                         import ICacheComponents

from pprint					import pprint

###########################
# Vision des zones
###########################
class CounterAppComps( ICloudMgrResolvers, IAppcodeGetters, IAeraGetters, IEnvGetters, IAppCompGetters, ICacheComponents, SequentialOps ):

   def __init__( self, appcode = '', le_appcode_provider = None, aera = '', le_aera_provider = None, env = '', le_env_provider = None, appcomp = '', le_appcomp_provider = None, resolvers = None, cache_components = None ):
      ICloudMgrResolvers.__init__( self, resolvers )
      IAppcodeGetters.__init__( self, appcode = appcode, le_appcode_provider = le_appcode_provider )
      IAeraGetters.__init__( self, aera = aera, le_aera_provider = le_aera_provider)
      IEnvGetters.__init__( self, env = env, le_env_provider = le_env_provider)
      IAppCompGetters.__init__( self, appcomp = appcomp, le_appcomp_provider = le_appcomp_provider )
      ICacheComponents.__init__( self, cache_components = cache_components )

      def get_cloudmap_in_a_list( cmr ):
         result = None
         with cmr as cloudmap_resolver:
            result = cloudmap_resolver.cloudmap.copy()
         return [ result ]

      def get_list_from_attribute( l, attribute = None ):
         l_result = []
         for e in l:
            result = []

            if getattr( self, attribute ):
            	result = e.get( getattr( self, attribute ), [] )
            else:
               result = e.values()

            if type( result ) == dict:
               result = [ result ]

            l_result.extend( result )
         return l_result 

      def sum_element_on_list( l ):
         result = 0
         for e in l:
            result = result + len( e )
         return result

      SequentialOps.__init__( 
         self, 
         self.cloudmap_resolver, 
         [ 
            get_cloudmap_in_a_list, 
            lambda l, attribute = 'aera': get_list_from_attribute( l, attribute ),
            lambda l, attribute = 'appcode': get_list_from_attribute( l, attribute ),
            lambda l, attribute = 'env': get_list_from_attribute( l, attribute ),
            lambda l, attribute = 'appcomp': get_list_from_attribute( l, attribute ),
            sum_element_on_list,
         ] 
      )

@presentation.render_for( CounterAppComps )
def render(self, h, comp, *args):
   with h.div( class_ = 'er_appcomps' ):

      with self.cloudmap_resolver as cloudmap_resolver:
         h << repr( self.operate() )

   return h.root