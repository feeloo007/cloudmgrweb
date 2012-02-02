# -*- coding: UTF-8 -*-
from __future__                                 import with_statement
from nagare                                     import presentation, var
from ajax_x_components                          import XComponentsUpdates
from pprint                                     import pprint
from i_dom_tree					import IDomTree


class FormRefreshOnComet( IDomTree ):
   def __init__( 
          self, 
          dom_storage, 
          dom_father 
       ):

      IDomTree.__init__( 
                  self, 
                  dom_storage = dom_storage, 
                  dom_father = dom_father 
               )

@presentation.render_for( FormRefreshOnComet )
def render(
       self, 
       h, 
       *args
    ):

   v_event_name = var.Var()
   v_appcode    = var.Var()
   v_aera       = var.Var()
   v_env        = var.Var()
   v_appcomp    = var.Var()

   def fake():
      pass

   with h.form( 
             id = 'refresh_on_comet_event' 
          ):

         #h << h.input( type = 'submit', class_ = 'submit', style = 'display: none ;' ).action( fake )

         h << h.input( 
                 type = 'submit', 
                 class_ = 'submit', 
                 style = 'display: none ;' 
              ).action( 
                 XComponentsUpdates( 
                    le_l_knowndiv = lambda: self.dom_storage.get_l_known_div_for_change( 
                                                                v_event_name(), 
                                                                appcode = v_appcode(),
                                                                aera = v_aera(), 
                                                                env = v_env(),
                                                                appcomp = v_appcomp() 
                                            ), 
                    update_himself = True, 
                    action = lambda: fake() 
                 ) 
              )

         h << h.input( 
                 type = 'hidden', 
                 class_ = 'event_name' 
              ).action( v_event_name )

         h << h.input(
                 type = 'hidden', 
                 class_ = 'appcode' 
              ).action( v_appcode )

         h << h.input( 
                 type = 'hidden', 
                 class_ = 'aera' 
              ).action( v_aera )

         h << h.input( 
                 type = 'hidden', 
                 class_ = 'env' 
              ).action( v_env )

         h << h.input( 
                 type = 'hidden', 
                 class_ = 'appcomp' 
         ).action( v_appcomp )

   return h.root

