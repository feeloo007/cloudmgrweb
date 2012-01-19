# -*- coding: UTF-8 -*-
from __future__ import with_statement

class IAppcodeGetters( object ):

   def __init__( self, appcode = '', le_appcode_provider = None ):
      self._appcode 		= appcode
      self._le_appcode_provider = le_appcode_provider

   def get_appcode( self ):
      if not self._le_appcode_provider:
         return self._appcode
      else:
         return self._le_appcode_provider()

   def set_appcode( self, appcode ):
     self._appcode = appcode

   appcode = property( get_appcode, set_appcode )


class IAeraGetters( object ):

   def __init__( self, aera = '', le_aera_provider = None ):
      self._aera 		= aera
      self._le_aera_provider 	= le_aera_provider

   def get_aera( self ):
      if not self._le_aera_provider:
         return self._aera
      else:
         return self._le_aera_provider()

   def set_aera( self, aera ):
     self._aera = aera

   aera = property( get_aera, set_aera )


class IEnvGetters( object ):

   def __init__( self, env = '', le_env_provider = None ):
      self._env                = env
      self._le_env_provider    = le_env_provider

   def get_env( self ):
      if not self._le_env_provider:
         return self._env
      else:
         return self._le_env_provider()

   def set_env( self, env ):
     self._env = env

   env = property( get_env, set_env )


class IAppCompGetters( object ):

   def __init__( self, appcomp = '', le_appcomp_provider = None ):
      self._appcomp                = appcomp
      self._le_appcomp_provider    = le_appcomp_provider

   def get_appcomp( self ):
      if not self._le_appcomp_provider:
         return self._appcomp
      else:
         return self._le_appcomp_provider()

   def set_appcomp( self, appcomp ):
     self._appcomp = appcomp

   appcomp = property( get_appcomp, set_appcomp )

