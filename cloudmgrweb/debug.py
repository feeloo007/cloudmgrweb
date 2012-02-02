# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import component, presentation

# Interaction comet
from i_comet                                    import ICloudMgrComet

from i_dom_tree                                 import IDomTree

from pprint                                     import pprint, pformat

from time					import localtime

from colorama					import init, Fore


class CloudmgrwebDebug(
         ICloudMgrComet,
         IDomTree,
      ):

   def __init__(
          self,
          dom_storage      = None,
          dom_father       = None,
          cloudmgrweb      = None,
       ):

      # Initialisation colorama
      init( autoreset = True )

      ICloudMgrComet.__init__(
                        self
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

   # Suppression des précédents fils
   # dans le modèle DOM
   self.delete_dom_childs()

   self.add_event_for_knowndiv( 
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
   print( Fore.BLUE + pformat( self._cloudmgrweb.d_dom_tree ) + Fore.RESET )
   print
   print
   print( Fore.CYAN +  pformat( self._cloudmgrweb.d_events ) + Fore.RESET )
   print
   print

   h << 'DEBUG IN STDOUT NAGARE-SERVE'

   return h.root

