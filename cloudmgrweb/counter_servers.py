# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component, ajax
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from cloudmgrlib.m_cmgr_cloudmap_resolver       import with_cloudmap_resolver
import i_getter
from cloudmgrlib.sequential_ops			import SequentialOps

# Interaction comet
from i_comet                                    import ICloudMgrComet
from nagare                                     import ajax

# Mise en place d'un DOM pour la gestion comet
from i_dom_tree                                 import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider

from pprint					import pprint

###########################
# Vision des zones
###########################
@i_getter.define_getter( 'appcode' )
@i_getter.define_getter( 'aera' )
@i_getter.define_getter( 'env' )
@i_getter.define_getter( 'appcomp' )
class CounterServers( 
         ICloudMgrResolvers, 
         ICloudMgrComet, 
         SequentialOps, 
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

      # Interaction comet
      ICloudMgrComet.__init__( 
         self 
      )

      IDynamicComponentProvider.__init__(
         self
      )

      IDomTree.__init__(
         self,
         dom_storage 	= dom_storage,
         dom_father 	= dom_father,
      )


      @with_cloudmap_resolver( self )
      def get_cloudmap_in_a_list( 
             *args,
             **kwargs 
          ):
         result = kwargs[ 'with_cloudmap_resolver' ].cloudmap.copy()
         return [ result ]

      def get_list_from_attribute( 
             l, 
             attribute = None 
          ):

         l_result = []
         for e in l:
            result = []

            if getattr( self, attribute ) and getattr( self, attribute ) <> '*':
            	result = e.get( 
                            getattr( 
                               self, 
                               attribute 
                            ), 
                            [] 
                         )
            else:
               result = e.values()

            if type( result ) == dict:
               result = [ result ]

            l_result.extend( result )
         return l_result 

      def print_struct( x ):
         pprint( x )
         print
         return x

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
            lambda l, attribute = 'aera': get_list_from_attribute( 
                                             l, 
                                             attribute 
                                          ),
            lambda l, attribute = 'appcode': get_list_from_attribute( 
                                                l, 
                                                attribute 
                                          ),
            lambda l, attribute = 'env': get_list_from_attribute( 
                                            l, 
                                            attribute 
                                         ),
            lambda l, attribute = 'appcomp': get_list_from_attribute( 
                                                l, 
                                                attribute 
                                             ),
            sum_element_on_list,
         ] 
      )

@presentation.render_for( CounterServers )
@with_cloudmap_resolver()
def render(
       self, 
       h, 
       comp, 
       *args,
       **kwargs
    ):

   self.reset_in_dom(
           comp
   )

   self.add_event_for_knowndiv(
      'REFRESH_ON_CREATION_SERVER_DEMAND', 
      self, 
      appcode 	= self.appcode, 
      env 	= self.env,
   )

   with h.div( class_ = 'counter_appcomps' ):

      h << repr( self.process() )

   return h.root
