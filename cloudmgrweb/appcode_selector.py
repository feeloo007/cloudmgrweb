# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, var, ajax

from ajax_x_components				import XComponentsUpdates

from pprint					import pprint

from i_dom_tree					import IDomTree

import i_getter


#########################
# Selection du code appli
#########################
@i_getter.define_getter( 'appcode' )
class AppcodeSelector( 
         IDomTree,         
      ):

  def __init__( 
         self,
         dom_storage 	= None,
         dom_father 	= None,
         *args, 
         **kwargs
      ):

     IDomTree.__init__(
        self,
        dom_storage 	= dom_storage,
        dom_father 	= dom_father,
     )


@presentation.render_for( AppcodeSelector )
def render(
       self, 
       h, 
       comp, 
       *args
    ):

   self.reset_in_dom(
           comp
   )

   v_appcode = var.Var()

   with h.div( 
           class_ = 'appcode_selector' 
        ):

      if self.appcode:

         h << h.div( 
                 self.appcode, class_ = 'message current' 
              )

      else:

         h << h.div( 
                 u'Saisir un code application :', 
                 class_ = 'message default' 
              )

      with h.form:

         with h.div( 
                 class_ = 'form' 
              ):

            h << h.input( 
                    type = 'text', 
                    class_ = 'input_appcode', 
                    value = self.appcode 
                 ).action( v_appcode )

            h << h.input( 
                    type = 'submit', 
                    value= u'Charger', 
                    class_ = 'submit_appcode' 
                 ).action( 
                    XComponentsUpdates(
                       le_l_knowndiv = lambda: self.dom_storage.get_l_known_div_for_change(
                                                                   'LOCAL_REFRESH_ON_APPCODE_SELECTED',
                                                                   appcode = v_appcode(),
                                               ),
                       update_himself = True,
                       action = lambda: self.set_appcode( 
                                           v_appcode()
                                        ),
                    )
                 )


   return h.root
