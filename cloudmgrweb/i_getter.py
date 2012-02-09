# -*- coding: UTF-8 -*-
from __future__ import with_statement
from pprint 	import pprint, pformat

def define_getter(
       accessor 
    ):

   def modify_class( 
      cl 
   ):


      # Définition de tous les noms utilisés
      # par la suite
      hide_attrib_accessor		= '__%s' % accessor
      init_param_accessor		= accessor
      mthd_get_accessor			= 'get_%s' % accessor
      mthd_set_accessor			= 'set_%s' % accessor
      prop_accessor			= accessor

      origin_init = cl.__init__

      def __init__( 
             self, 
             *args, 
	     **kwargs
          ):
   
         assert( kwargs.has_key( init_param_accessor ) ), u'%s doit exister' % init_param_accessor

         setattr( 
            self, 
            hide_attrib_accessor, 
            kwargs.get( 
                  init_param_accessor, 
                  '' 
               ) 
         )

         origin_init( 
            self, 
            *args, 
            **kwargs 
         )
         
      cl.__init__ = __init__


      # Création du accessor en lecture
      def get_accessor(
             self
          ):

         if not callable( 
                   getattr(
                      self,
                      hide_attrib_accessor,
                   )
                ):

            return getattr( 
                      self, 
                      hide_attrib_accessor 
                   )

         else:

            return getattr( 
                      self, 
                      hide_attrib_accessor 
                   )()

      # Création de l'accessor en écriture
      def set_accessor(
             self,
             value
          ):

         setattr( 
            self, 
            hide_attrib_accessor, 
            value 
         )

      # Ajout des méthodes d'accès à la class
      setattr(
         cl,
         mthd_get_accessor,
         get_accessor
      )

      setattr(
         cl,
         mthd_set_accessor,
         set_accessor
      )
     
      # Création de la propriété
      setattr(
         cl,
         prop_accessor,
         property( get_accessor, set_accessor )
      )

      return cl

   return modify_class
