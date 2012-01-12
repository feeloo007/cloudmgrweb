# -*- coding: UTF-8 -*-
from __future__ import with_statement
from nagare	import comet, ajax


class ICloudMgrComet( object ):

   def __init__( self ):

      if not comet.channels.get( 'cloudmgr' ):
         comet.channels.create( 'cloudmgr', 'cloudmgrweb_comet_refresh' )

   def get_comet_channel( self ):
      return comet.channels[ 'cloudmgr' ]

   comet_channel = property( get_comet_channel )
