# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component, ajax
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from i_controllers                              import IAppcodeGetters, IAeraGetters, IEnvGetters, IAppCompGetters
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
class CounterServers( 
         ICloudMgrResolvers, 
         ICloudMgrComet, 
         IAppcodeGetters, 
         IAeraGetters, 
         IEnvGetters, 
         IAppCompGetters, 
         SequentialOps, 
         IDomTree,
         IDynamicComponentProvider,
      ):

   def __init__(
          self, 
          appcode = '', 
          le_appcode_provider = None, 
          aera = '', 
          le_aera_provider = None, 
          env = '', 
          le_env_provider = None, 
          appcomp = '', 
          le_appcomp_provider = None, 
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

      IAeraGetters.__init__( 
         self, 
         aera = aera, 
         le_aera_provider = le_aera_provider
      )

      IEnvGetters.__init__( 
         self, 
         env = env, 
         le_env_provider = le_env_provider
      )

      IAppCompGetters.__init__( 
         self, 
         appcomp = appcomp, 
         le_appcomp_provider = le_appcomp_provider 
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
         dom_storage = dom_storage,
         dom_father = dom_father,
      )


      def get_cloudmap_in_a_list( 
             cmr 
          ):

         result = None
         with cmr as cloudmap_resolver:
            result = cloudmap_resolver.cloudmap.copy()
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

   def get_appcode( self ):
      if IAppcodeGetters.get_appcode( self ) == '':
         return '*'
      return IAppcodeGetters.get_appcode( self )

   def set_appcode( self, appcode ):
      IAppcodeGetters.set_appcode( 
         self, 
         appcode 
      )
   appcode = property( 
                get_appcode, 
                set_appcode 
             )

@presentation.render_for( CounterServers )
def render(
       self, 
       h, 
       comp, 
       *args
    ):

   self.delete_dom_childs()

   self.add_event_for_knowndiv(
      'REFRESH_ON_CREATION_SERVER_DEMAND', 
      self, 
      appcode = self.appcode, 
      env = self.env,
   )

   with h.div( class_ = 'counter_appcomps' ):

      with self.cloudmap_resolver as cloudmap_resolver:
         h << repr( self.process() )

   return h.root
