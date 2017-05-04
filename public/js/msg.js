/**
* Show success alert msg
*/


function displaySuccess(msg) {
    if(msg !== '') {
        $('#success_msg').removeClass('hidden').text(JSON.stringify(JSON.parse(msg),undefined,4)); 
     }    
}

function displayConfig(config) {
     if(config !== '') {
         
        var js = JSON.parse(config);
        $('#config').removeClass('hidden').text(config); 
     }         
    
}


