# -*- coding: UTF-8 -*-

from pprint import pprint

class IDomTree( object ):
   def __init__( self, dom_storage, dom_father ):

      if not dom_storage:

         self.d_dom_tree 	= {
         }

         self.d_events 		= {
         }

         self.dom_storage 	= self

      else:

         self.dom_storage 	= dom_storage

         self.d_dom_tree 	= self.dom_storage.d_dom_tree

         self.d_events 		= self.dom_storage.d_events
 
      self.d_dom_tree.setdefault(
            dom_father,
            {
               'dom_father': None
            },
      ).setdefault(
         'dom_childs',
         []
      ).append( self )
 
      self.d_dom_tree[ self ] = {
         'dom_father': dom_father,
         'dom_childs': [],
         'events': [],
      }

 
   def get_dom_storage( self ):
      return self.__dom_storage
 
   def set_dom_storage( self, dom_storage ):
      self.__dom_storage = dom_storage
 
   dom_storage = property( get_dom_storage, set_dom_storage )
 
   def get_dom_father( self ):
      return self.d_dom_tree[ self ][ 'dom_father' ]
 
   dom_father = property( get_dom_father )
 
   def get_d_dom_tree( self ):
      return self.__d_dom_tree
 
   def set_d_dom_tree( self, d_dom_tree ):
     self.__d_dom_tree = d_dom_tree
 
   d_dom_tree = property( get_d_dom_tree, set_d_dom_tree )
 
   def get_dom_childs( self ):
      return self.d_dom_tree[ self ][ 'dom_childs' ]
   
   dom_childs = property( get_dom_childs )
 
   def get_all_dom_childs( self ):
 
      def ready_to_reduce( l ):
         if l == []:
            return [ [ ] ]
         return l
       
      return reduce( list.__add__, ready_to_reduce( [ reduce( list.__add__, [ [ e ], e.all_dom_childs ] ) for e in self.dom_childs ] ) )
 
   all_dom_childs = property( get_all_dom_childs )
 
   def delete_dom_childs( self ):
 
      for dom_child in self.dom_childs[ : ]:
         dom_child.delete_events()
         dom_child.delete_dom_childs()
         self.d_dom_tree[ dom_child.dom_father ][ 'dom_childs' ].remove( dom_child )
         del( self.d_dom_tree[ dom_child ] )


   def get_d_events( self ):
      return self.__d_events

   def set_d_events( self, d_events ):
      self.__d_events = d_events

   d_events = property( get_d_events, set_d_events )

   def add_event_for_knowndiv( self, event_name, cp_knowndiv, appcode = '-', aera = '-', env = '-', appcomp = '-' ):

      self.d_dom_tree[ self ][ 'events' ].append( {
                                                      'event_name'	: event_name, 
                                                      'cp_knowndiv'	: cp_knowndiv,
                                                      'appcode'		: appcode, 
                                                      'aera'		: aera, 
					              'env'		: env, 
                                                      'appcomp'		: appcomp 
                                                  }
                                          )

      
      self.d_events.setdefault(
         event_name,
         {}
      ).setdefault(
         appcode,
         {}
      ).setdefault(
         aera,
         {}
      ).setdefault(
         env,
         {}
      ).setdefault(
         appcomp,
         {}
      )[ cp_knowndiv ] = lambda: cp_knowndiv.le_get_knowndiv()


   def delete_events( self ):

      for desc_event in self.d_dom_tree[ self ][ 'events' ]:

         del( self.d_events[ desc_event[ 'event_name' ] ][ desc_event[ 'appcode' ] ][ desc_event[ 'aera' ] ][ desc_event[ 'env' ] ][ desc_event[ 'appcomp' ] ][ desc_event[ 'cp_knowndiv' ] ] )

         if not self.d_events[ desc_event[ 'event_name' ] ][ desc_event[ 'appcode' ] ][ desc_event[ 'aera' ] ][ desc_event[ 'env' ] ][ desc_event[ 'appcomp' ] ]:
            del( self.d_events[ desc_event[ 'event_name' ] ][ desc_event[ 'appcode' ] ][ desc_event[ 'aera' ] ][ desc_event[ 'env' ] ][ desc_event[ 'appcomp' ] ] )
     
         if not self.d_events[ desc_event[ 'event_name' ] ][ desc_event[ 'appcode' ] ][ desc_event[ 'aera' ] ][ desc_event[ 'env' ] ]:
            del( self.d_events[ desc_event[ 'event_name' ] ][ desc_event[ 'appcode' ] ][ desc_event[ 'aera' ] ][ desc_event[ 'env' ] ] )

         if not self.d_events[ desc_event[ 'event_name' ] ][ desc_event[ 'appcode' ] ][ desc_event[ 'aera' ] ]:
            del( self.d_events[ desc_event[ 'event_name' ] ][ desc_event[ 'appcode' ] ][ desc_event[ 'aera' ] ] )

         if not self.d_events[ desc_event[ 'event_name' ] ][ desc_event[ 'appcode' ] ]:
            del( self.d_events[ desc_event[ 'event_name' ] ][ desc_event[ 'appcode' ] ] )

         if not self.d_events[ desc_event[ 'event_name' ] ]:
            del( self.d_events[ desc_event[ 'event_name' ] ] )

if __name__ == "__main__":
   class ROOT( IDomTree ):
      def __init__( self ):
         IDomTree.__init__( self, dom_storage = None, dom_father = None )

   root = ROOT() 
   pprint( root.d_dom_tree )
   print

   class LEVEL1( IDomTree ):
      def __init__( self, dom_storage, dom_father ):
         IDomTree.__init__( self, dom_storage = dom_storage, dom_father = dom_father )

   e1 = LEVEL1( dom_storage = root, dom_father = root )
   pprint( root.d_dom_tree )
   print
   e2 = LEVEL1( dom_storage = root, dom_father = root )
   pprint( root.d_dom_tree )
   print

   class LEVEL2( IDomTree ):
      def __init__( self, dom_storage, dom_father ):
         IDomTree.__init__( self, dom_storage = dom_storage, dom_father = dom_father )

   e1_1 = LEVEL2( dom_storage = root, dom_father = e1 )
   pprint( root.d_dom_tree )
   print
   e1_2 = LEVEL2( dom_storage = root,  dom_father = e2 )
   pprint( root.d_dom_tree )
   print
   e2_1 = LEVEL2( dom_storage = root, dom_father = e1 )
   pprint( root.d_dom_tree )
   print

   class LEVEL3( IDomTree ):
      def __init__( self, dom_storage, dom_father ):
         IDomTree.__init__( self, dom_storage = dom_storage, dom_father = dom_father )

   e1_1_1 = LEVEL3( dom_storage = root, dom_father = e1_1 )
   pprint( root.d_dom_tree )
   print

   pprint( 'root.dom_childs: %s' % root.dom_childs )
   print
   pprint( 'e1.dom_childs: %s' % e1.dom_childs )
   print
   pprint( 'e2.dom_childs: %s' % e2.dom_childs )
   print
   pprint( 'e1_1.dom_childs: %s' % e1_1.dom_childs )
   print
   pprint( 'e1_2.dom_childs: %s' % e1_2.dom_childs )
   print
   pprint( 'e2_1.dom_childs: %s' % e2_1.dom_childs )
   print
   pprint( 'e1_1_1.dom_childs: %s' % e1_1_1.dom_childs )
   print
   pprint( 'root.all_dom_childs: %s' % root.all_dom_childs )
   print
   pprint( 'e1.all_dom_childs: %s' % e1.all_dom_childs )
   print
   pprint( 'e2.all_dom_childs: %s' % e2.all_dom_childs )
   print
   pprint( 'e1_1.all_dom_childs: %s' % e1_1.all_dom_childs )
   print
   pprint( 'e1_2.all_dom_childs: %s' % e1_2.all_dom_childs )
   print
   pprint( 'e2_1.all_dom_childs: %s' % e2_1.all_dom_childs )
   print
   pprint( 'e1_1_1.all_dom_childs: %s' % e1_1_1.all_dom_childs )
   print
   pprint( 'root.all_dom_childs: %s' % root.all_dom_childs )
   print
   root.delete_dom_childs()
   pprint( 'root.all_dom_childs: %s' % root.all_dom_childs )
   print