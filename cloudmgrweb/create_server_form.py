# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component, ajax, util
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
from cloudmgrlib.m_cmgr_cloudmap_resolver       import with_cloudmap_resolver, with_cloudmap_resolver_for_render
import i_getter
from cloudmgrlib.m_cmgr_manage_virtual_stack    import create_next_dhcp_file_for, create_vm
from ajax_x_components                          import XComponentsUpdates

# Interaction comet
from i_comet					import ICloudMgrComet

from i_dom_tree                                 import IDomTree

from i_dynamic_component_provider               import IDynamicComponentProvider

import stackless

###########################
# Vision des zones
###########################
@i_getter.define_getter( 'appcode' )
@i_getter.define_getter( 'aera' )
@i_getter.define_getter( 'env' )
@i_getter.define_getter( 'appcomp' )
class CreateServerForm( 
         ICloudMgrResolvers, 
         ICloudMgrComet, 
         IDomTree,
         IDynamicComponentProvider 
      ):

   def __init__( 
          self, 
          resolvers 	= None, 
          dom_storage 	= None,
          dom_father 	= None,
          *args,
          **kwargs
       ):

      ICloudMgrResolvers.__init__(
         self, 
         resolvers 
      )

      ICloudMgrComet.__init__( 
                        self 
                     )

      IDomTree.__init__(
                  self,
                  dom_storage = dom_storage,
                  dom_father = dom_father,
               )

      IDynamicComponentProvider.__init__(
                                   self
                                )
      

@presentation.render_for( CreateServerForm )
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

   with h.div( 
          '', 
          class_ = 'create_server_form %s %s %s' % ( self.aera, self.env, self.appcomp ) 
        ):

      if not self.appcode:

         h << h.div( 
                 u'Veuillez selectionner un code application', 
                 class_ = 'appcodes message' 
              )

      elif not self.aera:

         h << h.div( 
                 u'Veuillez selectionner une zone', 
                 class_ = 'aeras message' 
              )

      elif not self.env:

         h << h.div( 
                 u'Veuillez selectionner un environnement', 
                 class_ = 'envs message' 
              )

      elif not self.appcomp:

         h << h.div( 
                 u'Veuillez selectionner un composant applicatif', 
                 class_ = 'appcomps message' 
              )

      else:

          with h.form():

             def to_validation_step():

                try:
                   comp.answer()
                except:
                    pass

             h << h.input( 
                     type='submit', 
                     class_ = 'message %s %s %s' % ( self.aera, self.env, self.appcomp ), 
                     value=u'Créer un serveur %s en %s pour %s' % ( 
                        self.appcomp_resolver.get_appcomp_desc( self.appcomp ), 
                        self.env_resolver.get_env_desc( self.env ).lower(), 
                        self.appcode 
                     ) 
                  ).action( lambda: to_validation_step() )

   return h.root

@presentation.render_for( CreateServerForm, model = 'splash_for_creation_first_time' )
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

   h << u'Demande de création'

   return h.root

@presentation.render_for( CreateServerForm, model = 'validate' )
@with_cloudmap_resolver_for_render
def render(
        self, 
        h, 
        comp, 
        *args,
        **kwargs
    ):
   

   with h.div( 
          '', 
          class_ = 'create_server_form %s %s %s' % ( self.aera, self.env, self.appcomp ) 
        ):

      if not self.appcode:

         h << h.div( 
                 u'Veuillez selectionner un code application', 
                 class_ = 'appcodes message' 
         )

      elif not self.aera:

         h << h.div( 
                 u'Veuillez selectionner une zone', 
                 class_ = 'aeras message' 
              )

      elif not self.env:

         h << h.div( 
                 u'Veuillez selectionner un environnement', 
                 class_ = 'envs message' 
              )

      elif not self.appcomp:

         h << h.div( 
                 u'Veuillez selectionner un composant applicatif', 
                 class_ = 'appcomps message' 
              )

      else:

         with h.form():

            def create_and_get_next_dhcp_file():

               self._creating_hostname = create_next_dhcp_file_for( 
                                            appcode 	= self.appcode, 
                                            aera 	= self.aera, 
                                            env 	= self.env, 
                                            appcomp 	= self.appcomp 
                                         )

               try:
                  comp.answer( True )
               except:
                  pass

            h << h.input( 
                    type='submit', 
                    class_ = 'message valid %s %s %s' % ( self.aera, self.env, self.appcomp ),
                    value=u'Confirmer' 
                 ).action( 
                    XComponentsUpdates( 
                       # Supprimer pour ne pas être redondant avec le message comet
                       #le_l_knowndiv = lambda: self.dom_storage.get_l_known_div_for_change(
                       #                           'REFRESH_ON_CREATION_SERVER_DEMAND',
                       #                           appcode 	= self.appcode,
                       #                           aera 	= self.aera,
                       #                           env 	= self.env,
                       #                           appcomp 	= self.appcomp,
                       #                        ), 
                       update_himself = True, 
                       action = lambda: create_and_get_next_dhcp_file() 
                    ) 
                 )

            def cancel():

               try:
                  comp.answer( False )
               except:
                  pass

            h << h.input( 
                    type='submit', 
                    class_ = 'message cancel %s %s %s' % ( self.aera, self.env, self.appcomp ), 
                    value=u'Annuler' 
                 ).action( lambda: cancel() )

   return h.root


@i_getter.define_getter( 'appcode' )
@i_getter.define_getter( 'aera' )
@i_getter.define_getter( 'env' )
@i_getter.define_getter( 'appcomp' )
class CreateServerTask( 
         component.Task, 
         ICloudMgrResolvers, 
         IDomTree,
         IDynamicComponentProvider, 
      ):

   def __init__( 
          self, 
          resolvers = None, 
          dom_storage = None,
          dom_father = None,
          *args,
          **kwargs
       ):

      ICloudMgrResolvers.__init__( 
                            self, 
                            resolvers 
                         )

      IDomTree.__init__(
                  self,
                  dom_storage = dom_storage,
                  dom_father = dom_father,
               )

      IDynamicComponentProvider.__init__(
                                   self
                                )

      @with_cloudmap_resolver( self )
      def create_cp_create_server_form(
             *args,
             **kwargs
          ):
         return component.Component( 
                   CreateServerForm( 
                      appcode 		= lambda: self.appcode, 
                      aera 		= lambda: self.aera, 
                      env 		= lambda: self.env, 
                      appcomp 		= lambda: self.appcomp, 
                      resolvers 	= self,
                      dom_storage 	= self,
                      dom_father 	= self,
                   ) 
                )   

      self.create_dynamic_component(
         'cp_create_server_form',
         create_cp_create_server_form
      )


   def go( self, comp ):

      self.reset_in_dom(
              comp
      )

      self.create_cp_create_server_form()

      def kill_task( **kwargs ):
         comp._channel.send_exception( TaskletExit )
         comp._channel.close()

      self.add_event_for_knowndiv(
         'LOCAL_REFRESH_ON_APPCODE_SELECTED',
         self,
         le_callback_update     = kill_task,
         appcode                = '*',
      )

      #try:
      if True:

         comp.call( 
            self.cp_create_server_form 
         )

         if comp.call(
            self.cp_create_server_form, model = 'validate'
         ):

            self.cp_create_server_form.o.comet_channel.send( 
               'REFRESH_ON_CREATION_SERVER_DEMAND appcode:%s aera:%s env:%s appcomp:%s' % ( self.appcode, self.aera, self.env, self.appcomp ) 
            )

         else:

            return

         def finish_on_last_call( **kwargs ):
            comp.answer()

         self.add_event_for_knowndiv(
            'REFRESH_ON_CREATION_SERVER_DEMAND',
            self,
            le_callback_update     = finish_on_last_call,
            appcode                = self.appcode,
            aera                   = self.aera,
            env                    = self.env,
            appcomp                = self.appcomp
         )

         comp.call(
            self.cp_create_server_form, model = 'splash_for_creation_first_time'
         )

      #except TaskletExit, te:
      #   print 'TaskletExit %s' % stackless.current
      #   raise te
