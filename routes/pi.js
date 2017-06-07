var PythonShell     = require('python-shell'); 
var constants       = require('../utils/constants');


/******************************************************************************************************************************************
* PI RESTART 
***********************************************/
exports.restart  = function(req, res)  {
     
    var opts = {  scriptPath: constants.python_pi_path  };
    res.clearCookie("config",{path:'/'});    
      
    PythonShell.run('restart_pi.py', opts, function (err, ress) {
      if (err) throw err;
       res.redirect('/');
    });
     
};

/******************************************************************************************************************************************
* PI SHUTDOWN
***********************************************/
exports.shutdown  = function(req, res)  { 
     
    var opts = {  scriptPath: constants.python_pi_path  }; 
    res.clearCookie("config",{path:'/'});    
    PythonShell.run('shutdown_pi.py', opts, function (err, ress) {
      if (err) throw err;
       res.redirect('/');
    });
     
};