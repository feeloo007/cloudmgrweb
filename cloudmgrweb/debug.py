# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import component, presentation

# Interaction comet
from i_comet                                    import ICloudMgrComet

from i_cache_components                         import ICacheComponents

# Mise en place d'un DOM pour la gestion comet
from i_dom                                      import IDom
from i_dom_tree                                 import IDomTree

from pprint                                     import pprint

from time					import localtime


class CloudmgrwebDebug(
         ICloudMgrComet,
         IDomTree,
         ICacheComponents,
         IDom,
      ):

   def __init__(
          self,
          cache_components = None,
          dom_storage      = None,
          dom_father       = None,
          cloudmgrweb      = None,
       ):

      ICloudMgrComet.__init__(
                        self
      )
 
      ICacheComponents.__init__( 
                          self, 
                          cache_components = cache_components 
      )

      IDom.__init__(
         self,
         dom_father = dom_father,
         dom_element_name = CloudmgrwebDebug.__name__,
         dom_complement_element_name = ''
      )

      IDomTree.__init__(
                  self,
                  dom_storage    = dom_storage,
                  dom_father     = dom_father,
      )

      self._cloudmgrweb = cloudmgrweb

@presentation.render_for( CloudmgrwebDebug )
def render(
       self,
       h,
       *args
    ):

   self.set_knowndiv_for( 
      '*', 
      self, 
      appcode = '*',
      aera = '*', 
      env = '*', 
      appcomp = '*' 
   )

   print( '##################################' )
   print( '##################################' )
   print( localtime() )
   print( '##################################' )
   print( '##################################' )
   pprint( self._cloudmgrweb.d_dom_tree )
   print
   print
   pprint( self._cloudmgrweb.d_events )
   print
   print

   h << 'DEBUG IN STDOUT NAGARE-SERVE'

   return h.root

