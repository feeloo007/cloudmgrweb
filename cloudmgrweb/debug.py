# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import component, presentation

# Interaction comet
from i_comet                                    import ICloudMgrComet

from i_dom_tree                                 import IDomTree

from pprint                                     import pprint, pformat

from time					import localtime

from colorama					import init, Fore, Back, Style

from ajax_x_components                          import XComponentsUpdates



import gc


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
       comp,
       *args
    ):

   # Suppression des précédents fils
   # dans le modèle DOM
   self.reset_in_dom(
           comp
   )

   self.add_event_for_knowndiv( 
      '*', 
      self, 
      appcode 	= '*',
      aera 	= '*', 
      env 	= '*', 
      appcomp 	= '*',
   )

   def print_gc():
      gc.collect( 0 )
      gc.collect( 1 )
      gc.collect( 2 )
      print( Fore.BLACK + Back.WHITE + Style.BRIGHT + pformat( gc.garbage ) + Style.RESET_ALL + Back.RESET + Fore.RESET )
      for o in gc.garbage:
         print( Fore.BLUE + Back.WHITE + Style.BRIGHT + pformat( gc.get_referrers( o ) ) + Style.RESET_ALL + Back.RESET + Fore.RESET )
         print( Fore.MAGENTA + Back.WHITE + Style.BRIGHT + pformat( gc.get_referents( o ) ) + Style.RESET_ALL + Back.RESET + Fore.RESET )
         

   #print( '##################################' )
   #print( '##################################' )
   #print( localtime() )
   #print( '##################################' )
   #print( '##################################' )
   #print( Fore.BLUE + pformat( self._cloudmgrweb.d_dom_tree ) + Fore.RESET )
   #print
   #print
   #print( Fore.CYAN +  pformat( self._cloudmgrweb.d_events ) + Fore.RESET )
   #print
   #print
   #print_gc()

   h << 'DEBUG IN STDOUT NAGARE-SERVE'


   #with h.form():
   #   h << h.input(
   #           type = 'submit',
   #           value= u'Print GC',
   #          ).action(
   #             XComponentsUpdates(
   #                update_himself = True,
   #                action = print_gc,
   #             )
   #          )



   return h.root

