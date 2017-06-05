var PythonShell     = require('python-shell');
var express         = require('express');
var router          = express.Router();
var repeat          = require('repeat');
 
var read_config     = require('../utils/read_config');
var utils           = require('../utils/browser');
var constants       = require('../utils/constants');


/******************************************************************************************************************************************
* Detections
***********************************************/
exports.load  = function(req, res) {
    
    // Detection type
    var type = req.params.type;
   
    // Get the eventual pagination parameters passed in argument
    var page; 
    page = (typeof req.query.page === "undefined")?1:req.query.page;  
    
    // Get all maybe detections
    var opts = {
        mode: 'json',
        args: ['/var/www/html/out/'+type+'/',page,constants.DETECTION_PER_PAGE],
        scriptPath: constants.python_path+'/detections'
    };
    
    // Test Browser
    browser = utils.get_browser(req)
      
    PythonShell.run('list_detection_files.py', opts, function (err, ress) {
      if (err) throw err;
      
      var org_url = req.protocol + '://' + req.get('host') + req.originalUrl;
      
      // Render options
      opts_render = {
            results: ress,
            folder: '/'+type,
            type:type,
            browser: browser,
            curURL: org_url.substring(0, org_url.indexOf('?')),
            title:(type==='maybe')?'Uncertain detections':((type==='false')?'False detections':'Fireballs')
      };
        
      if(typeof req.query.success !== "undefined") {
        opts_render.success = req.query.success.split("$");
      }
      
      read_config.load_page_with_conf_test_cam_pwd(res,'detections',opts_render);
    
    });
};

/******************************************************************************************************************************************
* Delete Detections (single)
***********************************************/
exports.delete_single_detect  = function(req, res) {
    
    // Detection type
    var type = req.params.type;
    var ev   = req.params.ev;
      
    // Get select detection 
    var opts = { 
        mode: 'text',
        args: ['/var/www/html/out/'+type+'/',ev],
        scriptPath: constants.python_path+'/file_management'
    };
    
    PythonShell.run('delete_file.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/detection/'+type+'?success='+ress[0]);
    });
     
};


/******************************************************************************************************************************************
* Detection false deletion (multiple)
***********************************************/
exports.delete_multiple_detect = function(req, res) { 
   
    // Detection type
    var type = req.params.type;
    var evs  = req.body.events;
   
    var opts = { 
        mode: 'text',
        args: ['/var/www/html/out/'+type+'/',evs],
        scriptPath: constants.python_path+'/file_management'
    }; 
     
    PythonShell.run('delete_file.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/detection/'+type+'?success='+ress[0]);
    });
     
};


/******************************************************************************************************************************************
* Detection ALL deletion  
***********************************************/
exports.delete_all_detect = function(req, res) { 
   
    // Detection type
    var type = req.params.type; 
   
    var opts = { 
        mode: 'text',
        args: ['/var/www/html/out/'+type+'/'],
        scriptPath: constants.python_path+'/file_management'
    }; 
     
    PythonShell.run('delete_file.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/detection/'+type+'?success='+ress[0]);
    });
     
};