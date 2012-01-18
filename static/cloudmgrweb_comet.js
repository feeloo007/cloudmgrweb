//function cloudmgrweb_comet_refresh( refresh_identification ) {
//
//   var l_tokens = refresh_identification.split( " " ) ;
//   var refresh_on_name = l_tokens.shift() ;
//
//   for ( i = 0; i < document.getElementsByName( refresh_on_name ).length; i++ ) {
//      var l_class = document.getElementsByName( refresh_on_name ).item( i ).className.split( ' ' ) ;
//
//      // Vérifions si le composant doit être notifié quelque soit les paramètres supplémentaires
//      if ( ( l_class.length == 1 ) && ( l_class[ 0 ] == 'ALL' ) ) {
//         document.getElementsByName( refresh_on_name ).item( i )[ 2 ].click() ;
//      }
//
//      // Vérifions si le composant possède strictement les mêmes classes
//      l_class_to_search	= l_tokens.sort().slice( 0 ) ;
//      l_class_found 	= l_class.sort().slice( 0 ) ;
//      for ( j = 0 ; j < l_class_to_search.length ; j++ ) {
//         for ( h = 0 ; h < l_class_found.length ; h++ ) {
//            if ( l_class_to_search[ j ] == l_class_found[ h ] ) {
//               l_class_to_search.splice( j, 1 ) ;
//               delete l_class_found.splice( h, 1 ) ;
//               j-- ;
//               break ;
//            }
//         }
//      } 
//      if ( l_class_to_search.length == 0 ) {
//         console.log( 'click' )
//         document.getElementsByName( refresh_on_name ).item( i )[ 2 ].click() ;
//      }
//   }
//}

function cloudmgrweb_comet_refresh( refresh_identification ) {
   console.log( refresh_identification )

   var form_id	 	= "refresh_on_comet_event" ;
   var event_name 	= "event_name" ;
   var l_params_name 	= [ "appcode", "aera", "env", "appcomp" ] ;
   var formsub_name 	= "submit" ;

   var l_tokens = refresh_identification.split( " " ) ;
   
   document.getElementById( form_id ).getElementsByClassName( event_name )[ 0 ].value = l_tokens.shift() ;

   var d_params = {} ;
   for ( i = 0 ; i < l_tokens.length; i++ ) {
      l_param_value = l_tokens[ i ].split( ":" ) ;
      d_params[ l_param_value[ 0 ] ] = l_param_value[ 1 ] ; 
   }

   for ( i = 0 ; i < l_params_name.length; i++ ) { 
      if ( d_params[ l_params_name[ i ] ] != null ) { 
         document.getElementById( form_id ).getElementsByClassName( l_params_name[ i ] )[ 0 ].value = d_params[ l_params_name[ i ] ] ;
      }
      else {
         document.getElementById( form_id ).getElementsByClassName( l_params_name[ i ] )[ 0 ].value = '*' ;
      }
   }

   document.getElementById( form_id ).getElementsByClassName( formsub_name )[ 0 ].click() ;

}
