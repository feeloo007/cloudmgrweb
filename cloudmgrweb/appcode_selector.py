# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, var, ajax
from ajax_x_components				import XComponentsUpdates

from pprint					import pprint

#########################
# Selection du code appli
#########################
class AppcodeSelector( object ):

  def __init__( self ):
     self._appcode = ''
     self._l_known_div_for_appcode_change = []

  def get_appcode( self ):
     return self._appcode

  def set_appcode( self, appcode ):
     self._appcode = appcode

  appcode = property( get_appcode, set_appcode )

  def register_known_div_for_appcode_change( self, cp_kd ):
     """
        Enregistre un KnownDiv
        On doit y trouver les attributs :
        .o.id
        .o.component
     """
     self._l_known_div_for_appcode_change.append( cp_kd )

  def get_l_known_div_for_appcode_change( self ):
     return self._l_known_div_for_appcode_change



@presentation.render_for( AppcodeSelector )
def render(self, h, comp, *args):

   v_appcode = var.Var()

   with h.div( class_ = 'appcode_selector' ):

      if self.appcode:
         h << h.div( self.appcode, class_ = 'message current' )
      else:
         h << h.div( u'Saisir un code application :', class_ = 'message default' )

      with h.form:
         with h.div( class_ = 'form' ):
            h << h.input( type = 'text', class_ = 'input_appcode', value = self.appcode ).action( v_appcode )
            h << h.input( type = 'submit', value= u'Charger', class_ = 'submit_appcode' ).action( XComponentsUpdates( le_l_knowndiv = lambda: self.get_l_known_div_for_appcode_change(), update_himself = True, action = lambda: self.set_appcode( v_appcode() ) ) )

   return h.root
