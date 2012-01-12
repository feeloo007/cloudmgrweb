function cloudmgrweb_comet_refresh( refresh_identification ) {

   var l_tokens = refresh_identification.split( " " ) ;
   var refresh_on_name = l_tokens.shift() ;

   for ( i = 0; i < document.getElementsByName( refresh_on_name ).length; i++ ) {
      var l_class = document.getElementsByName( refresh_on_name ).item( i ).className.split( ' ' ) ;

      // Vérifions si le composant doit être notifié quelque soit les paramètres supplémentaires
      if ( ( l_class.length == 1 ) && ( l_class[ 0 ] == 'ALL' ) ) {
         document.getElementsByName( refresh_on_name ).item( i )[ 2 ].click() ;
      }

      // Vérifions si le composant possède strictement les mêmes classes
      l_class_to_search	= l_tokens.sort().slice( 0 ) ;
      l_class_found 	= l_class.sort().slice( 0 ) ;
      for ( j = 0 ; j < l_class_to_search.length ; j++ ) {
         for ( h = 0 ; h < l_class_found.length ; h++ ) {
            if ( l_class_to_search[ j ] == l_class_found[ h ] ) {
               l_class_to_search.splice( j, 1 ) ;
               delete l_class_found.splice( h, 1 ) ;
               j-- ;
               break ;
            }
         }
      } 
      if ( l_class_to_search.length == 0 ) {
         console.log( 'click' )
         document.getElementsByName( refresh_on_name ).item( i )[ 2 ].click() ;
      }
   }
}
