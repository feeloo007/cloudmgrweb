# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component, ajax, util
from ajax_x_components				import KnownDiv
from cloudmgrlib.i_cmgr_resolvers		import ICloudMgrResolvers
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
def render(
       self, 
       h, 
       comp, 
       *args
    ):

   self.reset_in_dom(
           comp
   )

   with self.cloudmap_resolver:

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

@presentation.render_for( CreateServerForm, model = 'validate' )
def render(
        self, 
        h, 
        comp, 
        *args
    ):
   
   with self.cloudmap_resolver:

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

      def create_cp_create_server_form():
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

      #try:
      if True:

         while True:

            stackless._gc_untrack( stackless.current )

            comp.call( 
               self.cp_create_server_form 
            )

            stackless._gc_untrack( stackless.current )

            if comp.call(
                  self.cp_create_server_form, model = 'validate'
               ):

               stackless._gc_untrack( stackless.current )

               self.cp_create_server_form.o.comet_channel.send( 
                  'REFRESH_ON_CREATION_SERVER_DEMAND appcode:%s aera:%s env:%s appcomp:%s' % ( self.appcode, self.aera, self.env, self.appcomp ) 
               )

            else:

               stackless._gc_untrack( stackless.current )

               continue

      #except TaskletExit, te:
      #   import stackless
      #   print 'TaskletExit %s' % stackless.current
      #   raise te
