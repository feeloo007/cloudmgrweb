# -*- coding: UTF-8 -*-
from __future__ import with_statement

import os
from nagare                                     import presentation, component, util, var, ajax, namespaces
from nagare.namespaces                          import xhtml

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

   def register_known_div_for_appcode_change( self, kd ):
       """
          Enregistre un objet qui doit respecter l'interface de KnownDiv concernant les objets
          .o.id
          .o.component
       """
       self._l_known_div_for_appcode_change.append( kd )

   def get_l_known_div_for_appcode_change( self ):
       return self._l_known_div_for_appcode_change


@presentation.render_for( AppcodeSelector )
def render(self, h, comp, *args):

    v_appcode = var.Var()

    if self.appcode:
        h << h.div( self.appcode )
    else:
        h << h.div( u'Saisir un code application :' )

    with h.form:
       h << h.input( type = 'text' ).action( v_appcode )
       h << h.input( type = 'submit', value= u'Charger' ).action( AppcodeUpdates( self, action = lambda: self.set_appcode( v_appcode() ) ) )

    return h.root



class AppcodeUpdates( ajax.Update ):
    """
       Classe à laquelle on passe une action
       qui exécute l'action et renvoit plusieurs flux de mises à jour
    """
    def __init__(self, appcode_selector, **kw ):
        self._appcode_selector = appcode_selector
        self._action = kw.get('action', lambda *args: None)
        super( AppcodeUpdates, self ).__init__( action=self.action, with_request=True )
        print '%s.__init__' % AppcodeUpdates

    def action(self, request, response, *args ):
        print '%s.action' % AppcodeUpdates.__class__

        if self._action:
            self._action( *args )


    def _generate_render( self, renderer ):
        """Generate the rendering function

        In:
          - ``renderer`` -- the current renderer

        Return:
          - the rendering function
        """

        # On alimente le tableau des rendus avec le rendu de l'update courant
        renders = [ super( AppcodeUpdates, self )._generate_render( renderer ) ]

        def ViewsToJs( r ):
            # On ajoute les rendus des composants tiers
            for cp in self._appcode_selector.get_l_known_div_for_appcode_change():
                renders.append( ajax.Update( lambda r: cp.o.component.render( r ), lambda: None, cp.o.id )._generate_render( r ) )
            return ajax.ViewsToJs( [ render( r ) for render in renders ] )

	return lambda r: ViewsToJs( r )


####e######################
# Vision des zones
###########################
class AerasViewer( object ):

   def __init__( self ):
       self._appcode = ''
       self._le_appcode_provider = None

   def get_appcode( self ):
       if not self._le_appcode_provider:
           return self._appcode
       else:
           return self._le_appcode_provider()

   def set_appcode( self, appcode ):
       self._appcode = appcode

   appcode = property( get_appcode, set_appcode )


   def set_appcode_provider( self, le ):
       """
          Permet d'écraser la méthode get d'accès à appcode
       """
       self._le_appcode_provider = le


@presentation.render_for( AerasViewer )
def render(self, h, comp, *args):
   h << self.appcode
   return h.root


class AlwaysDivAsyncRenderer( xhtml.AsyncRenderer ):
    def __init__(self, *args, **kw):
        super( AlwaysDivAsyncRenderer, self ).__init__( *args, **kw )
        self.wrapper_to_generate = True


#########################
# Div récupérant le numéro d'id du composant 
#########################
class KnownDiv( object ):
    def __init__( self, cp ):
        self._cp = cp
        self._id = None

    def get_id( self ):
        return self._id
    id = property( get_id )

    def get_component( self ):
        return self._cp

    component = property( get_component )


@presentation.render_for( KnownDiv )
def render(self, h, comp, *args):

    h << self._cp.render( AlwaysDivAsyncRenderer( h ) )
    self._id = h.root.get( 'id' )

    return h.root


class Cloudmgrweb(object):
    def __init__( self ):
        self._cp_appcode_selector 	= component.Component( AppcodeSelector() )
        self._cp_aeras_viewer		= component.Component( AerasViewer() )
        self._cp_aeras_viewer.o.set_appcode_provider( lambda: self._cp_appcode_selector.o.appcode )


@presentation.render_for(Cloudmgrweb)
def render(self, h, *args):

    cp_div_appcode_selector	= component.Component( KnownDiv( self._cp_appcode_selector ) )
    cp_div_aeras_viewer	        = component.Component( KnownDiv( self._cp_aeras_viewer ) )

    h << cp_div_appcode_selector
    h << cp_div_aeras_viewer

    self._cp_appcode_selector.o.register_known_div_for_appcode_change( cp_div_aeras_viewer )

    return h.root

# ---------------------------------------------------------------

app = Cloudmgrweb
