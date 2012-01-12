# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component, ajax, util
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from i_controllers                              import IAppcodeGetters, IAeraGetters, IEnvGetters, IAppCompGetters
from cloudmgrlib.m_cmgr_manage_virtual_stack    import create_next_dhcp_file_for, create_vm
from ajax_x_components                          import XComponentsUpdates

# Interaction comet
from i_comet					import ICloudMgrComet

###########################
# Vision des zones
###########################
class CreateServerForm( ICloudMgrResolvers, IAppcodeGetters, IAeraGetters, IEnvGetters, IAppCompGetters, ICloudMgrComet ):

   def __init__( self, appcode = '', le_appcode_provider = None, aera = '', le_aera_provider = None, env = '', le_env_provider = None, appcomp = '', le_appcomp_provider = None, resolvers = None ):
      ICloudMgrResolvers.__init__( self, resolvers )
      IAppcodeGetters.__init__( self, appcode = appcode, le_appcode_provider = le_appcode_provider )
      IAeraGetters.__init__( self, aera = aera, le_aera_provider = le_aera_provider )
      IEnvGetters.__init__( self, env = env, le_env_provider = le_env_provider )
      IAppCompGetters.__init__( self, appcomp = appcomp, le_appcomp_provider = le_appcomp_provider )

      # Interaction comet
      ICloudMgrComet.__init__( self )

      self._l_le_known_div_for_change = []
      self._known_component_for_answer = None

   def get_l_known_div_for_change( self ):
       return [ le() for le in self._l_le_known_div_for_change ]

   def register_le_known_div_for_change( self, le_kd ):
       """
          Enregistre une lambda expression renvoyant un KnownDiv
          Une fois la lambda expression instanciée, on doit y trouver les attributs :
          .o.id
          .o.component
       """
       self._l_le_known_div_for_change.append( le_kd )


   def get_known_component_for_answer( self ):
       print 'get_known_component_for_answer %s' % self._known_component_for_answer
       return self._known_component_for_answer

   def set_known_component_for_answer( self, le_comp ):
       self._known_component_for_answer = le_comp
       print 'set_known_component_for_answer %s' % self._known_component_for_answer

@presentation.render_for( CreateServerForm )
def render(self, h, comp, *args):

   with h.div( '', class_ = 'create_server_form %s %s %s' % ( self.aera, self.env, self.appcomp ) ):
      if not self.appcode:
         h << h.div( u'Veuillez selectionner un code application', class_ = 'appcodes message' )
      if not self.aera:
         h << h.div( u'Veuillez selectionner une zone', class_ = 'aeras message' )
      if not self.env:
         h << h.div( u'Veuillez selectionner un environnement', class_ = 'envs message' )
      if not self.appcomp:
         h << h.div( u'Veuillez selectionner un composant applicatif', class_ = 'appcomps message' )
      else:
         with self.cloudmap_resolver as cloudmap_resolver:
           with h.form():
              def to_validation_step():
                 try:
                    comp.answer()
                 except:
                    pass
              h << h.input( type='submit', class_ = 'message %s %s %s' % ( self.aera, self.env, self.appcomp ), value=u'Créer un serveur %s en %s pour %s' % ( self.appcomp_resolver.get_appcomp_desc( self.appcomp ), self.env_resolver.get_env_desc( self.env ).lower(), self.appcode ) ).action( lambda: to_validation_step() )

   return h.root

@presentation.render_for( CreateServerForm, model = 'validate' )
def render(self, h, comp, *args):
   
   with h.div( '', class_ = 'create_server_form %s %s %s' % ( self.aera, self.env, self.appcomp ) ):
      if not self.appcode:
         h << h.div( u'Veuillez selectionner un code application', class_ = 'appcodes message' )
      if not self.aera:
         h << h.div( u'Veuillez selectionner une zone', class_ = 'aeras message' )
      if not self.env:
         h << h.div( u'Veuillez selectionner un environnement', class_ = 'envs message' )
      if not self.appcomp:
         h << h.div( u'Veuillez selectionner un composant applicatif', class_ = 'appcomps message' )
      else:
         with self.cloudmap_resolver as cloudmap_resolver:
            with h.form():
               def create_and_get_next_dhcp_file():
                  self._creating_hostname = create_next_dhcp_file_for( appcode = self.appcode, aera = self.aera, env = self.env, appcomp = self.appcomp )
                  try:
                     comp.answer( True )
                  except:
                     pass

               h << h.input( type='submit', class_ = 'message valid %s %s %s' % ( self.aera, self.env, self.appcomp ), value=u'Confirmer' ).action( XComponentsUpdates( le_l_knowndiv = lambda: self.get_l_known_div_for_change(), update_himself = False, action = lambda: create_and_get_next_dhcp_file() ) )

               def cancel():
                  try:
                     comp.answer( False )
                  except:
                     pass
               h << h.input( type='submit', class_ = 'message cancel %s %s %s' % ( self.aera, self.env, self.appcomp ), value=u'Annuler' ).action( lambda: cancel() )

   return h.root


class CreateServerTask( component.Task, ICloudMgrResolvers, IAppcodeGetters, IAeraGetters, IEnvGetters, IAppCompGetters ):

   def __init__( self, appcode = '', le_appcode_provider = None, aera = '', le_aera_provider = None, env = '', le_env_provider = None, appcomp = '', le_appcomp_provider = None, resolvers = None ):
      ICloudMgrResolvers.__init__( self, resolvers )
      IAppcodeGetters.__init__( self, appcode = appcode, le_appcode_provider = le_appcode_provider )
      IAeraGetters.__init__( self, aera = aera, le_aera_provider = le_aera_provider )
      IEnvGetters.__init__( self, env = env, le_env_provider = le_env_provider )
      IAppCompGetters.__init__( self, appcomp = appcomp, le_appcomp_provider = le_appcomp_provider )

      self._cp_create_server_form = component.Component( CreateServerForm( le_appcode_provider = lambda: self.appcode, le_aera_provider = lambda: self.aera, le_env_provider = lambda: self.env, le_appcomp_provider = lambda: self.appcomp, resolvers = resolvers ) )

   def get_l_known_div_for_change( self ):
       return [ le() for le in self._cp_create_server_form.o.get_l_known_div_for_change() ]

   def register_le_known_div_for_change( self, le_kd ):
       """
          Enregistre une lambda expression renvoyant un KnownDiv
          Une fois la lambda expression instanciée, on doit y trouver les attributs :
          .o.id
          .o.component
       """
       self._cp_create_server_form.o.register_le_known_div_for_change( le_kd )


   def go( self, comp ):

      while True:

         comp.call( self._cp_create_server_form )
         if comp.call( self._cp_create_server_form, model='validate' ):
            self._cp_create_server_form.o.comet_channel.send( 'REFRESH_ON_CREATION_SERVER_DEMAND %s %s %s %s' % ( self.appcode, self.aera, self.env, self.appcomp ) )
         else:
            continue
