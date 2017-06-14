var PythonShell     = require('python-shell'); 
var constants       = require('../utils/constants');
var cookie          = require('../utils/cookie');


/******************************************************************************************************************************************
* Diplay Update Page
***********************************************/
exports.load  = function(req, res)  {
   var pjson = require(constants.APP_PATH+'/package.json');
   cookie.get_config_cookie_and_render(req, res, {  info: pjson}, 'appli');    
};


/******************************************************************************************************************************************
* UPDATE
***********************************************/
exports.update  = function(req, res)  {
     
     
     PythonShell.run('update.py', {
            scriptPath: constants.python_path+'/setup',
            uid:0,
            gid:0
     }, function (err, results) {
          if (err) throw err;
          // results is an array consisting of messages collected during execution
          console.log('results: %j', results);
    });
     
     
    
};