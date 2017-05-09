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
 
bodyParser = require('body-parser')

// Views
app.set('views', [path.join(__dirname + '/public/actions'),path.join(__dirname + '/public/home'),path.join(__dirname + '/public'),'/var/www/html/out']); 
app.set('view engine', 'ejs');


// Bower
app.use('/bower_components', express.static(__dirname + '/bower_components'));

app.use(bodyParser.urlencoded({
    extended: true
}));



/**********************************************
* Chrome or Firefox - detect browser
***********************************************/ 
function get_browser(req) {
    var ua = req.headers['user-agent'];
    var parser = new UAParser();
    return parser.setUA(ua).getBrowser().name; 
}
 

/**********************************************
* Home Page
***********************************************/
app.get('/', function(req, res) {
    
    // Test Browser
    browser = get_browser(req)
    
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
   

/**********************************************
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
                
                console.log(message_success);
                
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


/**********************************************
* Detection maybe
***********************************************/
app.get('/detection/maybe', function(req, res) {
    
    // Get all maybe detections
    var opts = {
        mode: 'json',
        args: ['/var/www/html/out/maybe/'] 
    };
    
    // Test Browser
    browser = get_browser(req)
 
     
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




/*
app.get('/signIn', function(req, res) {
    res.sendFile('signin.html', {
        'root': __dirname + '/public/signin'
    });
});
 
 
 
 

app.post('/register', function(req, resp) {
    var _firstName = req.body.inputFirstName;
    var _lastName = req.body.inputLastName;
    var _username = req.body.inputUsername;
    var _password = req.body.inputPassword;
    var _phone = req.body.inputPhone;

    var options = {
        url: 'http://192.168.0.27:3000/user/',
        method: 'POST',
        auth: {
            user: 'admin',
            password: 'admin'
        },
        formData: {
            firstname: _firstName,
            lastname: _lastName,
            username: _username,
            password: _password,
            phone: _phone
        }
    }

    request(options, function(err, res, body) {
        if (err) {
            return resp.render('screenshot', {
                error: err
            })
        }
        var result = JSON.parse(body)
        if (result._status == 'ERR') {
            if (result._error.code == '400') {
                return resp.render('screenshot', {
                    error: 'Username Already Exists!'
                })
            }
            return resp.render('screenshot', {
                error: result._issues.username
            })
        } else {
            console.log('All good');
            resp.redirect('http://localhost:3000/#/signin');
        }
    })
});
*/

app.listen(3000)
