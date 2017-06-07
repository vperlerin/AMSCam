var constants       = require('../utils/constants');
var read_config     = require('./read_config');
var child_process   = require('child_process');
 
module.exports = {
     
    // Return config from cookie 
    // or read config.txt, create cookie and return the result
    get_config_cookie_and_render: function (req, res, template_opts, template_name) {
        var cookie = req.cookies.config;  
    
        
        if (cookie === undefined) {
             
            read_config.read_config(function(config) {
              
                res.cookie('config', config, {path:'/'});
                template_opts.config = config;
                
                if(template_name==="home") {
                     
                    child_process.exec(constants.python_path +  'simple-capture-status.sh', function(error, stdout, stderr){
                        template_opts.capture = stdout;   
                        res.render(template_name,template_opts); 
                    });
                    
                 } else {
               
                    res.render(template_name,template_opts);
                }
             }); 
            
             
        } else  {
            // yes, cookie was already present 
            template_opts.config = cookie;
                
                if(template_name==="home") {
                     
                    child_process.exec(constants.python_path +  'simple-capture-status.sh', function(error, stdout, stderr){
                        template_opts.capture = stdout;   
                        res.render(template_name,template_opts); 
                    });
                    
                 } else {
               
                    res.render(template_name,template_opts);
                }
        }  
 
        
    } 
    
}