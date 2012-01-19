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
