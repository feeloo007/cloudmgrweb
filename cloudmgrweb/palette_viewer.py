# -*- coding: UTF-8 -*-
from __future__ import with_statement

from nagare                                     import presentation, component

###########################
# Vision des zones
###########################
class PaletteViewer( object ):

   def __init__( self ):
      pass

@presentation.render_for( PaletteViewer )
def render(self, h, comp, *args):

   with h.div( style='display: table;' ):
      with h.div( style='display: table-row;' ):
         h << h.div( '#000000', style='background-color: #000000; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#434343', style='background-color: #434343; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#666666', style='background-color: #666666; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#999999', style='background-color: #999999; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#B7B7B7', style='background-color: #B7B7B7; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#CCCCCC', style='background-color: #CCCCCC; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#D9D9D9', style='background-color: #D9D9D9; color: black; display: table-cell ; padding: 1em;' )
         h << h.div( '#EFEFEF', style='background-color: #EFEFEF; color: black; display: table-cell ; padding: 1em;' )
         h << h.div( '#F3F3F3', style='background-color: #F3F3F3; color: black; display: table-cell ; padding: 1em;' )
      with h.div( style='display: table-row;' ):
         h << h.div( '#E6B8AF', style='background-color: #E6B8AF; color: black; display: table-cell ; padding: 1em;' )
         h << h.div( '#DD7E6B', style='background-color: #DD7E6B; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#CC4125', style='background-color: #CC4125; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#A61C00', style='background-color: #A61C00; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#85200C', style='background-color: #85200C; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#980000', style='background-color: #980000; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#5B0F00', style='background-color: #5B0F00; color: white; display: table-cell ; padding: 1em;' )
      with h.div( style='display: table-row;' ):
         h << h.div( '#F4CCCC', style='background-color: #F4CCCC; color: black; display: table-cell ; padding: 1em;' )
         h << h.div( '#EA9999', style='background-color: #EA9999; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#E06666', style='background-color: #E06666; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#CC0000', style='background-color: #CC0000; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#990000', style='background-color: #990000; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#660000', style='background-color: #660000; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#FF0000', style='background-color: #FF0000; color: white; display: table-cell ; padding: 1em;' )
      with h.div( style='display: table-row;' ):
         h << h.div( '#D9EAD3', style='background-color: #D9EAD3; color: black; display: table-cell ; padding: 1em;' )
         h << h.div( '#B6D7A8', style='background-color: #B6D7A8; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#93C47D', style='background-color: #93C47D; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#6AA84F', style='background-color: #6AA84F; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#38761D', style='background-color: #38761D; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#274E13', style='background-color: #274E13; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#00FF00', style='background-color: #00FF00; color: white; display: table-cell ; padding: 1em;' )
      with h.div( style='display: table-row;' ):
         h << h.div( '#D0E0E3', style='background-color: #D0E0E3; color: black; display: table-cell ; padding: 1em;' )
         h << h.div( '#A2C4C9', style='background-color: #A2C4C9; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#76A5AF', style='background-color: #76A5AF; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#45818E', style='background-color: #45818E; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#134F5C', style='background-color: #134F5C; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#0C343D', style='background-color: #0C343D; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#00FFFF', style='background-color: #00FFFF; color: white; display: table-cell ; padding: 1em;' )
      with h.div( style='display: table-row;' ):
         h << h.div( '#C9DAF8', style='background-color: #C9DAF8; color: black; display: table-cell ; padding: 1em;' )
         h << h.div( '#A4C2F4', style='background-color: #A4C2F4; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#6D9EEB', style='background-color: #6D9EEB; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#3C78D8', style='background-color: #3C78D8; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#285BAC', style='background-color: #285BAC; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#1C4587', style='background-color: #1C4587; color: white; display: table-cell ; padding: 1em;' )
         h << h.div( '#4A86E8', style='background-color: #4A86E8; color: white; display: table-cell ; padding: 1em;' )
   
   return h.root
