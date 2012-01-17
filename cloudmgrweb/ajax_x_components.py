# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, ajax
from nagare.namespaces                          import xhtml

class AlwaysDivAsyncRenderer( xhtml.AsyncRenderer ):
    """
       Classe héritant de AsyncRenderer et pour laquelle 
       wrapper_to_generate est à True
       Ceci permet de toujours avoir une div 
       autour des composants
    """
    def __init__(self, *args, **kw):
        super( AlwaysDivAsyncRenderer, self ).__init__( *args, **kw )
        self.wrapper_to_generate = True


class KnownDiv( object ):
    """
       Classe utilisant le rendu AlwaysDivAsyncRenderer pour
       le composant cp et récupérant l'id de la div associée
    """
    def __init__( self, cp ):
        self._cp = cp
        self._id = None

        def get_knowndiv():
           return self
        self._cp.o.le_get_knowndiv = get_knowndiv

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


class XComponentsUpdates( ajax.Update ):
    """
       Classe recevant en paramètre le_l_knowndiv
       Une lambda expression renvoyant une liste de KnownDiv
       qui seront modifiés
    """
    def __init__(self, le_l_knowndiv = [], update_himself = True, **kw ):
        self._le_l_knowndiv = le_l_knowndiv
        self._action = kw.get('action', lambda *args: None)
        self._update_himself = update_himself
        super( XComponentsUpdates, self ).__init__( action=self.action, with_request=True )
        
    def action(self, request, response, *args ):
        
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
        renders = [ super( XComponentsUpdates, self )._generate_render( renderer ) ]

        def ViewsToJs( r ):
            # On ajoute les rendus des composants tiers
            # au moment ou la requête est soumise

            # On supprime la mise à jour du composant lui même
            # au cas où son rendu ne serait pas nécessaire
            # (cas d'un composant mettantà jour son père)
            if not self._update_himself:
                renders.pop()
            if self._le_l_knowndiv:
                for kd in self._le_l_knowndiv():
                    print kd.id
                    def le_render( r, kd ):
                       return kd.component.render( r )
                    renders.append( ajax.Update( lambda r, kd=kd: le_render( r, kd ), lambda: None, kd.id )._generate_render( r ) )
            print ajax.ViewsToJs( [ render( r ) for render in renders ] )
            return ajax.ViewsToJs( [ render( r ) for render in renders ] )

        return lambda r: ViewsToJs( r )
