# -*- coding: UTF-8 -*-
from __future__ import with_statement
from pprint 	import pprint, pformat

def define_accessor(
       accessor 
    ):

   def modify_class( 
      cl 
   ):


      # Définitino de tous les noms utilisés
      # par la suite
      hide_attrib_accessor		= '__%s' % accessor
      hide_le_attrib_accessor_provider	= '__le_%s_provider' % accessor
      init_param_accessor		= accessor
      init_le_accessor_provider		= 'le_%s_provider' % accessor
      mthd_get_accessor			= 'get_%s' % accessor
      mthd_set_accessor			= 'set_%s' % accessor
      prop_accessor			= accessor

      origin_init = cl.__init__

      def __init__( 
             self, 
             *args, 
	     **kwargs
          ):

         setattr( 
            self, 
            hide_attrib_accessor, 
            kwargs.get( 
                  init_param_accessor, 
                  '' 
               ) 
         )

         setattr( 
            self, 
            hide_le_attrib_accessor_provider, 
            kwargs.get( 
                  init_le_accessor_provider, 
                  None
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

         if not getattr( 
                   self, 
                   hide_le_attrib_accessor_provider 
                ):

            return getattr( 
                      self, 
                      hide_attrib_accessor 
                   )

         else:

            return getattr( 
                      self, 
                      hide_le_attrib_accessor_provider 
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


class IGetters:

   def __init__( 
      self, 
      *args, 
      **kwargs 
   ):
      pass


@define_accessor( 'appcode' )
class IAppcodeGetters(
         IGetters
      ):
    pass

@define_accessor( 'aera' )
class IAeraGetters(
         IGetters
      ):
    pass

@define_accessor( 'env' )
class IEnvGetters(
         IGetters
      ):
    pass

@define_accessor( 'appcomp' )
class IAppCompGetters(
         IGetters
      ):
    pass


if __name__ == "__main__":

   test_appcode = IAppcodeGetters( appcode = 'A01' )
   pprint( dir ( test_appcode ) )
   pprint( test_appcode.appcode )
