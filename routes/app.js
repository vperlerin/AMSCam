var PythonShell     = require('python-shell'); 
var constants       = require('../utils/constants');
var cookie          = require('../utils/cookie');


/******************************************************************************************************************************************
* Diplay Update Page
***********************************************/
exports.load  = function(req, res)  {
   var pjson = require(constants.APP_PATH+'/package.json');
   cookie.get_config_cookie_and_render(req, res, { info: pjson}, 'appli');    
};


/******************************************************************************************************************************************
* UPDATE
***********************************************/
exports.update  = function(req, res)  {
    
     PythonShell.run(constants.python_path+'/setup/update.py', { uid: 0 }, function (err, results) {
        console.log(results);
     });
  
    
};