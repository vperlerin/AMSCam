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
          // Redirect to the restart page
          res.redirect('/app/restart');
    });
      
};


/******************************************************************************************************************************************
* RESTART
***********************************************/
exports.restart  = function(req, res)  {
     return cookie.get_config_cookie_and_render(req, res, {}, 'restart');
};

/******************************************************************************************************************************************
* CRASH (real 'forever' restart)
***********************************************/
exports.crash  = function(req, res)  {
    PythonShell.run('restart.py', {
            scriptPath: constants.python_path+'/setup',
            uid:0,
            gid:0
     }, function (err, results) {
          if (err) throw err;
          // Redirect to login (but it won't happen)
          res.redirect('/');
    });
};