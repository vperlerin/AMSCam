var express = require('express'),
    app = express(),
    path = require('path'),
    request = require('request'),
    PythonShell = require('python-shell'),
    UAParser = require('ua-parser-js');

app.use(express.static(__dirname + '/public'));

// Img & Videos
app.use('/py_img',express.static('../../../var/www/html/out'));
app.use('/maybe',express.static('../../../var/www/html/out/maybe'));
app.use('/false',express.static('../../../var/www/html/out/false'));
app.use('/fireballs',express.static('../../../var/www/html/out/fireballs'));
 
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
    
    var pyshellUpload = new PythonShell('../fireball_camera/read_config.py', {
            mode: 'json' 
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
 
        var pyshellUpload = new PythonShell('../fireball_camera/latest.py', {
            mode: 'text' 
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
* Detection maybe
***********************************************/
app.get('/detection/maybe', function(req, res) {
    
    // Get all maybe detections
    var opts = {
        mode: 'json',
        args: ['/var/www/html/out/maybe/'] 
    };
    
    // Test Browser
    browser = utils.get_browser(req)
      
    PythonShell.run('../fireball_camera/list_files.py', opts, function (err, ress) {
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
        args: ['/var/www/html/out/maybe/',req.query.ev]
    }; 
    
    PythonShell.run('../fireball_camera/delete_file.py', opts, function (err, ress) {
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
        args: ['/var/www/html/out/maybe/',req.body.events]
    }; 
     
    PythonShell.run('../fireball_camera/delete_file.py', opts, function (err, ress) {
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
        args: ['/var/www/html/out/false/'] 
    };
    
    // Test Browser
    browser = utils.get_browser(req)
      
    PythonShell.run('../fireball_camera/list_files.py', opts, function (err, ress) {
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
        args: ['/var/www/html/out/false/',req.query.ev]
    }; 
    
    PythonShell.run('../fireball_camera/delete_file.py', opts, function (err, ress) {
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
        args: ['/var/www/html/out/false/',req.body.events]
    }; 
     
    PythonShell.run('../fireball_camera/delete_file.py', opts, function (err, ress) {
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
        args: ['/var/www/html/out/fireballs/'] 
    };
    
    // Test Browser
    browser = utils.get_browser(req)
      
    PythonShell.run('../fireball_camera/list_files.py', opts, function (err, ress) {
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
        args: ['/var/www/html/out/fireballs/',req.query.ev]
    }; 
    
    PythonShell.run('../fireball_camera/delete_file.py', opts, function (err, ress) {
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
        args: ['/var/www/html/out/fireballs/',req.body.events]
    }; 
     
    PythonShell.run('../fireball_camera/delete_file.py', opts, function (err, ress) {
        if (err) throw err;
        res.redirect('/detection/fireballs?success='+ress[0]);
    });
     
});
app.listen(3000);