# -*- coding: UTF-8 -*-

from pprint 			import pprint, pformat
from cloudmgrlib.sequential_ops import SequentialOps

from colorama			import init, Fore

class IDomTree( object ):

   def __init__( 
          self, 
          dom_storage, 
          dom_father 
       ):

      # Initialisation colorama
      init( autoreset = True )

      if not dom_storage:

         self.d_dom_tree 	= { }

         self.d_events 		= { }

         self.dom_storage 	= self

      else:

         self.dom_storage 	= dom_storage

         self.d_dom_tree 	= self.dom_storage.d_dom_tree

         self.d_events 		= self.dom_storage.d_events
 
      self.d_dom_tree.setdefault(
         dom_father,
         {
            'dom_father'	: None,
            'dom_fathers'	: [],
         },
      ).setdefault(
         'dom_childs',
         []
      ).append( self )

      self.d_dom_tree[ self ] = {
         'dom_father'	: dom_father,
         'dom_fathers'	: reduce(
                             list.__add__,
                             [ 
                                [ dom_father ], 
                                self.d_dom_tree[ dom_father ][ 'dom_fathers' ] 
                             ]
                          ),
         'dom_childs'	: [],
         'events'	: [],
      }


   def get_dom_storage( self ):
      return self.__dom_storage
 
   def set_dom_storage( self, dom_storage ):
      self.__dom_storage = dom_storage
 
   dom_storage = property( get_dom_storage, set_dom_storage )
 
   def get_dom_father( self ):
      #return self.d_dom_tree[ self ][ 'dom_father' ]
      if not self.d_dom_tree[ self ][ 'dom_fathers' ]:
         return None
      else:
         self.d_dom_tree[ self ][ 'dom_fathers' ][ 0 ]
 
   dom_father = property( get_dom_father )

   def get_dom_fathers( self ):
      return self.d_dom_tree[ self ][ 'dom_fathers' ][ : ]
     

   dom_fathers = property( get_dom_fathers )
 
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
 

   def reset_in_dom( self ):

      self.delete_events()

      for dom_child in self.dom_childs[ : ]:
         dom_child.delete_events()
         dom_child.reset_in_dom()
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

      for desc_event in self.d_dom_tree[ self ][ 'events' ][ : ]:

         del( self.d_events[ desc_event[ 'event_name' ] ][ desc_event[ 'appcode' ] ][ desc_event[ 'aera' ] ][ desc_event[ 'env' ] ][ desc_event[ 'appcomp' ] ][ desc_event[ 'cp_knowndiv' ] ] )
 
         self.d_dom_tree[ self ][ 'events' ].remove( desc_event )

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


   def get_l_known_div_for_change( self, event_name, appcode = '*', aera = '*', env = '*', appcomp = '*' ):

      def get_list_from_key( l, key ):
         l_result = []
         for e in l:
            result = []

            if e <> '*':
               result = e.get( key, [] )
            else:
               result = e.values()

            if type( result ) == dict:
               result = [ result ]

            l_result.extend( result )

            result = []
            result = e.get( '*', [] )

            if type( result ) == dict:
               result = [ result ]

            l_result.extend( result )

            result = []
            result = e.get( '-', [] )

            if type( result ) == dict:
               result = [ result ]

            l_result.extend( result )

         return l_result

      def print_struct( x ):
         print( Fore.YELLOW + pformat( x ) + Fore.RESET )
         print
         return x

      def to_one_list( l ):
         l_result = []
         for d in l:
            for k, v in d.items():
               l_result.append( { k: v } )
         return l_result

      def better_father( f1, f2 ):
         return f1

      def find_upper_fathers( l ):
         l_result = []
         for d in l: 
            if not l_result:
               l_result.append(
                  d
               )
               print( Fore.BLUE + pformat( l_result ) + Fore.RESET )

            for possible_father in [ d_possible_father.keys()[ 0 ] for d_possible_father in l_result ] :
               better_father(  d.keys()[ 0 ], possible_father )

         print( Fore.CYAN + pformat( l_result ) + Fore.RESET )
         return l_result

      def to_list_le( l ):
         l_result = []
         for d in l:
            result = None
            result = d.values()
            if type( result ) == dict:
               result = [ result ]
            l_result.extend( result )
         return l_result

      def process_list_le( l ):
         return [ le() for le in l ]

      seq = SequentialOps(
         [ self.d_events ],
         [
            lambda l, key = event_name: get_list_from_key( l, key ),
            lambda l, key = appcode: get_list_from_key( l, key ),
            lambda l, key = aera: get_list_from_key( l, key ),
            lambda l, key = env: get_list_from_key( l, key ),
            lambda l, key = appcomp: get_list_from_key( l, key ),
            #print_struct,
            #to_one_list,
            #print_struct,
            #find_upper_fathers,
            to_list_le,
            #print_struct,
            process_list_le,
         ]
      )

      return seq.process()



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
   root.reset_in_dom()
   pprint( 'root.all_dom_childs: %s' % root.all_dom_childs )
   print
