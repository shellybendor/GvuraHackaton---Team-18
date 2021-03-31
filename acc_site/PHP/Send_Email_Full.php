<?php
 
/*
 * Following code will create a new group row
 */
 
// array for JSON response
$response = array();
 
// check for required fields

     
	
$check = false;

function spamcheck($field)
  {
  //filter_var() sanitizes the e-mail
  //address using FILTER_SANITIZE_EMAIL
  $field=filter_var($field, FILTER_SANITIZE_EMAIL);

  //filter_var() validates the e-mail
  //address using FILTER_VALIDATE_EMAIL
  if(filter_var($field, FILTER_VALIDATE_EMAIL))
    {
    return TRUE;
    }
	  else
		{
		return FALSE;
		}
  }

    $mailcheck = spamcheck(isset($_POST['email']));
  
if (isset($_POST['subject']) && isset($_POST['message']) && isset($_POST['AppName']) && $mailcheck==FALSE)
  {//if "email" is filled out, proceed

  $email = $_POST['email'];
  $subject = $_POST['subject'];
  $message = $_POST['message'];
  $AppName = $_POST['AppName'];
  
  
  if( strlen(utf8_decode($message)) <= 15  || strpos($message, ' ') !== false )
  {
  
    mail("accomplishsoftwareinfo@gmail.com", "Email from $AppName:  $subject",
    $message, "From: $email" );   
	
	$check = true;
  } 
  

    // check if row inserted or not
    if ($check) {
        // successfully inserted into database
        $response["success"] = 1;
        $response["message"] = "Email successfully sent.";

        // echoing JSON response
        echo json_encode($response);
    } else {
        // failed to insert row
        $response["success"] = 0;
        $response["message"] = "Oops! An error occurred.";
 
        // echoing JSON response
        echo json_encode($response);
    }
} else {
    // required field is missing
    $response["success"] = 0;
    $response["message"] = "Required field(s) is missing";
 
    // echoing JSON response
    echo json_encode($response);
}

?>