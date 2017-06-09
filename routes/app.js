var PythonShell     = require('python-shell'); 
var constants       = require('../utils/constants');
var cookie          = require('../utils/cookie');


/******************************************************************************************************************************************
* Diplay Update Page
***********************************************/
exports.load  = function(req, res)  {
   var pjson = require(constants.APP_PATH+'/package.json');
   cookie.get_config_cookie_and_render(req, res, {  version: pjson.version}, 'appli');    
};


/******************************************************************************************************************************************
* UPDATE
***********************************************/
exports.update  = function(req, res)  {
    
     var pyshellUpload = new PythonShell('update.py', {
            scriptPath: constants.python_path+'/setup'
     });
     pyshellUpload.on('message', function (message_success) { 
            // Nothing here as the app will shut down anymay
     });
    
};