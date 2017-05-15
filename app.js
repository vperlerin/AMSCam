var express = require('express'),
    app = express(),
    path = require('path'),
    request = require('request'),
    PythonShell = require('python-shell'),
    UAParser = require('ua-parser-js'),
    constants = require("./constants");

app.use(express.static(__dirname + '/public'));

// Img & Videos
app.use('/py_img',express.static(path.join(__dirname + '/../../../var/www/html/out')));
app.use('/maybe',express.static(path.join(__dirname + '/../../../var/www/html/out/maybe')));
app.use('/false',express.static(path.join(__dirname + '/../../../var/www/html/out/false')));
app.use('/fireballs',express.static(path.join(__dirname + '/../../../var/www/html/out/fireballs')));
 
bodyParser = require('body-parser')

// Views
app.set('views', [
    path.join(__dirname + '/public/actions'),
    path.join(__dirname + '/public/home'),
    path.join(__dirname + '/public'),
    '/var/www/html/out']
); 
app.set('view engine', 'ejs');


// Bower
app.use('/bower_components', express.static(__dirname + '/bower_components'));

app.use(bodyParser.urlencoded({
    extended: true
}));
 
 
// Functions
var utils = require('./utils/browser');  


 

/******************************************************************************************************************************************
* Home Page
***********************************************/
app.get('/', function(req, res) {
    
    // Test Browser
    browser = utils.get_browser(req)
    
    console.log(__dirname);
    
    var pyshellUpload = new PythonShell('read_config.py', {
            mode: 'json',
            scriptPath: constants.python_path 
    });
     
    // Read config
    pyshellUpload.on('message',  function (config) { 
         res.render('home', {
            browser:  browser,
            config_info: config
        }) 
    });
    
});
   


/******************************************************************************************************************************************
* Screenshot Page
***********************************************/
app.get('/screenshot', function(req, res) {
    res.render('screenshot', {
        error: '',
        message_success: ''
    })
});


/**********************************************
* Take screenshot
***********************************************/
app.post('/screenshot', function(req, resp) {
 
        var pyshellUpload = new PythonShell('latest.py', {
            mode: 'text' ,
            scriptPath: constants.python_path 
         });
        
        // JSON.stringify(message_success, null, '\t')
        pyshellUpload.on('message',  function (message_success) { 
            if (message_success) {
                return resp.render('screenshot', {
                    message_success: message_success,
                    error: ''
                }) 
            }        
        });
        
        pyshellUpload.end(function (err) {
            console.log('screenshot FINISHED');
        });
          
});




/******************************************************************************************************************************************
* PI RESTART 
***********************************************/
app.get('/pi/restart', function(req, res) {
     
    var opts = {  scriptPath: constants.python_pi_path  };
  
    browser = utils.get_browser(req)
      
    PythonShell.run('restart_pi.py', opts, function (err, ress) {
      if (err) throw err;
       res.redirect('/');
    });
     
});

/******************************************************************************************************************************************
* PI SHUTDOWN
***********************************************/
app.get('/pi/shutdown', function(req, res) {
     
    var opts = {  scriptPath: constants.python_pi_path  };
  
    browser = utils.get_browser(req)
      
    PythonShell.run('shutdown_pi.py', opts, function (err, ress) {
      if (err) throw err;
       res.redirect('/');
    });
     
});



/******************************************************************************************************************************************
* Detection maybe
***********************************************/
app.get('/detection/maybe', function(req, res) {
    
    // Get all maybe detections
    var opts = {
        mode: 'json',
        args: ['/var/www/html/out/maybe/'],
        scriptPath: constants.python_path
    };
    
    // Test Browser
    browser = utils.get_browser(req)
      
    PythonShell.run('list_files.py', opts, function (err, ress) {
      if (err) throw err;
      
      // Render options
      opts_render = {
            results: ress,
            folder: '/maybe',
            browser: browser
      };
        
      if(typeof req.query.success !== "undefined") {
        opts_render.success = req.query.success.split("$");
      }
           
       res.render('maybe', opts_render) 
    });
     
});


/**********************************************
* Detection maybe deletion (single)
***********************************************/
app.get('/detection/maybe/delete', function(req, res) {
    
    // Get select detection 
    var opts = { 
        mode: 'text',
        args: ['/var/www/html/out/maybe/',req.query.ev],
        scriptPath: constants.python_path
    }; 
    
    PythonShell.run('delete_file.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/detection/maybe?success='+ress[0]);
    });
      
});


/**********************************************
* Detection maybe deletion (multiple)
***********************************************/
app.post('/detection/maybe/delete_multiple', function(req, res) {
   
    var opts = { 
        mode: 'text',
        args: ['/var/www/html/out/maybe/',req.body.events],
        scriptPath: constants.python_path
    }; 
     
    PythonShell.run('delete_file.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/detection/maybe?success='+ress[0]);
    });
     
});



/******************************************************************************************************************************************
* Detection false
***********************************************/
app.get('/detection/false', function(req, res) {
    
    // Get all maybe detections
    var opts = {
        mode: 'json',
        args: ['/var/www/html/out/false/'],
        scriptPath: constants.python_path
    };
    
    // Test Browser
    browser = utils.get_browser(req)
      
    PythonShell.run('list_files.py', opts, function (err, ress) {
      if (err) throw err;
      
      // Render options
      opts_render = {
            results: ress,
            folder: '/false',
            browser: false
      };
        
      if(typeof req.query.success !== "undefined") {
        opts_render.success = req.query.success.split("$");
      }
           
       res.render('false', opts_render) 
    });
     
});


/**********************************************
* Detection false deletion (single)
***********************************************/
app.get('/detection/false/delete', function(req, res) {
    
    // Get select detection 
    var opts = { 
        mode: 'text',
        args: ['/var/www/html/out/false/',req.query.ev],
        scriptPath: constants.python_path
    };
    
    PythonShell.run('delete_file.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/detection/false?success='+ress[0]);
    });
      
});


/**********************************************
* Detection false deletion (multiple)
***********************************************/
app.post('/detection/false/delete_multiple', function(req, res) {
   
    var opts = { 
        mode: 'text',
        args: ['/var/www/html/out/false/',req.body.events],
        scriptPath: constants.python_path
    }; 
     
    PythonShell.run('delete_file.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/detection/false?success='+ress[0]);
    });
     
});

  
/******************************************************************************************************************************************
* Detection fireball
***********************************************/
app.get('/detection/fireballs', function(req, res) {
    
    // Get all maybe detections
    var opts = {
        mode: 'json',
        args: ['/var/www/html/out/fireballs/'] ,
        scriptPath: constants.python_path 

    };
    
    // Test Browser
    browser = utils.get_browser(req)
      
    PythonShell.run('list_files.py', opts, function (err, ress) {
      if (err) throw err;
      
      // Render options
      opts_render = {
            results: ress,
            folder: '/fireballs',
            browser: false
      };
        
      if(typeof req.query.success !== "undefined") {
        opts_render.success = req.query.success.split("$");
      }
           
       res.render('fireballs', opts_render) 
    });
     
});


/**********************************************
* Detection false deletion (single)
***********************************************/
app.get('/detection/fireballs/delete', function(req, res) {
    
    // Get select detection 
    var opts = { 
        mode: 'text',
        args: ['/var/www/html/out/fireballs/',req.query.ev],
        scriptPath: constants.python_path 
    }; 
    
    PythonShell.run('delete_file.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/detection/fireballs?success='+ress[0]);
    });
      
});


/**********************************************
* Detection false deletion (multiple)
***********************************************/
app.post('/detection/fireballs/delete_multiple', function(req, res) {
   
    var opts = { 
        mode: 'text',
        args: ['/var/www/html/out/fireballs/',req.body.events],
        scriptPath: constants.python_path 
    }; 
     
    PythonShell.run('delete_file.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/detection/fireballs?success='+ress[0]);
    });
     
});
app.listen(3000);