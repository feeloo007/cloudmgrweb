# -*- coding: UTF-8 -*-

from cloudmgrlib.sequential_ops import SequentialOps

from nagare			import component

import stackless

from pprint 			import pprint, pformat

from colorama			import Fore, Back, Style

class IDomTree( object ):

   def __init__( 
          self, 
          dom_storage, 
          dom_father 
       ):

      self.previous_comp	= None

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
            'dom_fathers'	: [],
            'events'		: [],
         },
      ).setdefault(
         'dom_childs',
         []
      ).append( self )

      self.d_dom_tree[ self ] = {
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


   def get_dom_storage( 
          self 
       ):

      return self.__dom_storage
 

   def set_dom_storage( 
          self, 
          dom_storage 
       ):

      self.__dom_storage = dom_storage
 

   dom_storage = property( get_dom_storage, set_dom_storage )
 

   def get_dom_father( 
          self 
       ):

      if not self.d_dom_tree[ self ][ 'dom_fathers' ]:
         return None
      else:
         return self.d_dom_tree[ self ][ 'dom_fathers' ][ 0 ]
 

   dom_father = property( get_dom_father )


   def get_dom_fathers( 
          self 
       ):

      return self.d_dom_tree[ self ][ 'dom_fathers' ]
     

   dom_fathers = property( get_dom_fathers )
 

   def get_d_dom_tree( 
          self 
       ):

      return self.__d_dom_tree
 
   def set_d_dom_tree( 
          self, 
          d_dom_tree 
       ):

     self.__d_dom_tree = d_dom_tree
 

   d_dom_tree = property( get_d_dom_tree, set_d_dom_tree )

 
   def get_dom_childs( 
          self 
       ):

      return self.d_dom_tree[ self ][ 'dom_childs' ]
   

   dom_childs = property( get_dom_childs )
 

   def get_all_dom_childs( 
          self 
       ):
 
      def ready_to_reduce( l ):
         if l == []:
            return [ [ ] ]
         return l
       
      return reduce( 
                list.__add__, 
                ready_to_reduce( 
                   [ reduce( 
                        list.__add__, 
                        [ 
                           [ e ], 
                           e.all_dom_childs 
                        ] 
                     ) for e in self.dom_childs 
                   ] 
                ) 
             )
 

   all_dom_childs = property( get_all_dom_childs )


   def get_previous_comp(
          self
       ):
      return self.__previous_comp


   def set_previous_comp(
          self,
          previous_comp
       ):
      self.__previous_comp = previous_comp

   previous_comp = property( get_previous_comp, set_previous_comp )


   def get_previous_channel( 
          self,
       ):
      if self.previous_comp:
         return self.previous_comp._channel
      else:
         return None

   previous_channel = property( get_previous_channel )
 

   def reset_in_dom( 
          self,
          comp, 
       ):

      # Permet de ne pas conserver une référence
      # permanente sur ce tasklet
      stackless._gc_untrack( stackless.current )

      # Permet de tuer le tasklet précédemment attaché à la Task
      if isinstance( self, component.Task ) and self.previous_channel and not self.previous_channel.closed and not self.previous_channel.closing:
         self.previous_channel.send_exception( TaskletExit )
         self.previous_channel.close()

      # suppression des évènemenets associés
      self.delete_events()

      # Appel récursif vers les enfants
      for dom_child in self.dom_childs[ : ]:

         dom_child.delete_events()

         dom_child.reset_in_dom(
                      None
         )

         self.d_dom_tree[ dom_child.dom_father ][ 'dom_childs' ].remove( dom_child )

         del( self.d_dom_tree[ dom_child ] )

         del( dom_child )

      self.previous_comp = comp


   def get_d_events( 
          self 
        ):

      return self.__d_events

   def set_d_events( 
          self, 
          d_events 
       ):

      self.__d_events = d_events


   d_events = property( get_d_events, set_d_events )

   def fake( **d_params_for_update ):
      pass


   def add_event_for_knowndiv( 
          self, 
          event_name, 
          cp_knowndiv, 
          le_callback_update 	= fake,
          appcode 		= '-', 
          aera 			= '-', 
          env 			= '-', 
          appcomp 		= '-', 
       ):

      self.d_dom_tree[ self ][ 'events' ].append( {
                                                      'event_name'		: event_name, 
                                                      'cp_knowndiv'		: cp_knowndiv,
                                                      'le_callback_update' 	: le_callback_update,
                                                      'appcode'			: appcode, 
                                                      'aera'			: aera, 
					              'env'			: env, 
                                                      'appcomp'			: appcomp 
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


   def delete_events( 
          self 
       ):


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


   def get_l_known_div_for_change( 
          self, 
          event_name, 
          appcode 	= '*', 
          aera 		= '*', 
          env 		= '*', 
          appcomp 	= '*' 
       ):

      d_params_for_update = {
         'appcode': 	appcode,
	 'aera':	aera,
	 'env':		env,
	 'appcomp':	appcomp,
      }

      def process_le_callback_updates(
             l,
      ):
     
         for d in reduce(
                     list.__add__,
                     map(
                        lambda e: self.d_dom_tree[ e ][ 'events' ],
                        map( 
                           lambda o: o.keys()[ 0 ],
                           l
                        )
                     )
                  ): 

            if d[ 'event_name' ] == event_name:

               d[ 'le_callback_update' ]( **d_params_for_update )

         
         return l


      def get_list_from_key( 
             l, 
             key 
          ):

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


      def print_struct( 
             x, 
             color = Fore.BLACK + Back.WHITE + Style.BRIGHT 
          ):

         print(
            color + pformat( x ) + Style.RESET_ALL + Back.RESET + Fore.RESET
         )
         return x


      def to_one_list( 
             l 
          ):

         l_result = []

         for d in l:

            for k, v in d.items():

               if { k: v } not in l_result:

                  l_result.append( { k: v } )

         return l_result


      def find_upper_fathers( 
             l 
          ):

         l_result = []

         for d in l: 

            if not l_result:
               l_result.append(
                  d
               )

            try:

               for d_possible_father in l_result[ : ]:

                  if d_possible_father.keys()[ 0 ] in d.keys()[ 0 ].dom_fathers:
                     raise Exception( 'NOVALID' )

                  if d.keys()[ 0 ] in d_possible_father.keys()[ 0 ].dom_fathers:
                     l_result.remove( d_possible_father )

               if d not in l_result:
                  l_result.append( d )

            except Exception, e:
               pass

         return l_result


      def to_list_le( 
             l 
          ):

         l_result = []

         for d in l:

            result = None
            result = d.values()

            if type( result ) == dict:
               result = [ result ]

            l_result.extend( result )

         return l_result


      def process_list_le( 
             l 
          ):

         return [ le() for le in l ]

      seq = SequentialOps(
         [ self.d_events ],
         [
            lambda l, key 	= event_name: 	get_list_from_key( l, key ),
            lambda l, key 	= appcode: 	get_list_from_key( l, key ),
            lambda l, key 	= aera: 	get_list_from_key( l, key ),
            lambda l, key 	= env: 		get_list_from_key( l, key ),
            lambda l, key 	= appcomp: 	get_list_from_key( l, key ),
            to_one_list,
            process_le_callback_updates,
            find_upper_fathers,
            #lambda l, color 	= Fore.CYAN: 	print_struct( l, color ),
            to_list_le,
            process_list_le,
            #lambda l, color 	= Fore.WHITE: 	print_struct( l, color ),
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
