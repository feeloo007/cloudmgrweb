# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers               import ICloudMgrResolvers
from cloudmgrlib.m_cmgr_cloudmap_resolver       import with_cloudmap_resolver, with_cloudmap_resolver_for_render
import i_getter

from i_dom_tree                                 import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider

from pprint                                     import pprint


###########################
# Vision des zones
###########################
@i_getter.define_getter( 'appcode' )
@i_getter.define_getter( 'aera' )
@i_getter.define_getter( 'env' )
@i_getter.define_getter( 'appcomp' )
@i_getter.define_getter( 'num_component' )
@i_getter.define_getter( 'd_component_status' )
class ServerViewer( 
         ICloudMgrResolvers, 
         IDomTree,
         IDynamicComponentProvider,
      ):

   def __init__( 
          self, 
          resolvers 		= None, 
          dom_storage 		= None,
          dom_father 		= None,
          *args,
          **kwargs
       ):

      ICloudMgrResolvers.__init__( 
         self, 
         resolvers 
      )

      IDomTree.__init__(
         self,
         dom_storage 	= dom_storage,
         dom_father 	= dom_father,
      )

      IDynamicComponentProvider.__init__(
         self
      )

      self.__servername 	= '%s-%s-%s' % ( 
                                     self.appcomp, 
                                     self.num_component, 
                                     self.aera 
                                  )


   def get_servername( self ):
      return self.__servername
   servername = property( get_servername )


@presentation.render_for( ServerViewer )
@with_cloudmap_resolver_for_render
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

   with h.div( class_='component %s %s %s %s' % ( self.aera, self.env, self.appcomp, self.servername ) ):
      with h.table():
         with h.tr():
            with h.td(): 
               with h.div( class_ = 'description' ):
                  h << '%s' % ( self.servername )
         with h.tr():
            with h.td(): 
               with h.div():
                  pass
   return h.root
