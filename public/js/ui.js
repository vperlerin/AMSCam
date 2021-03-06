

function test_one_selected($table) {
   if($table.find('input[type=checkbox]:checked').length==0) {
        $('button[data-action=delete-all]').prop('disabled',true);
   } else {
        $('button[data-action=delete-all]').prop('disabled',false);
   } 
}

function confirm_before($this) {
    var url = $this.attr('href');
    bootbox.confirm({
        message: $this.attr('data-confirm'),
        buttons: {
            confirm: {
                label: 'Yes',
                className: 'btn-danger'
            },
            cancel: {
                label: 'No',
                className: 'btn-default'
            }
        },
        callback: function (result) {
            if(result){
                window.location =  url;   
            }
        }
    });   
}


$(function() {
    
 
    
   // Action to confirm (link with href)
   $('[data-confirm]').click(function(e) {
        e.stopPropagation();
        confirm_before($(this));
        return false; 
   });
     
   // Load for screenshot 
   $('.load-on-click').click(function(e) {
       $(this).html('<span class="fa fa-spinner fa-spin"></span>');
       var attr = $(this).attr('loader-text');
       if(typeof attr !== typeof undefined && attr !== false) {
            $('#loader').html('<div><span class="fa fa-spinner fa-pulse fa-5x fa-fw"></span><br/><h2 class="text-center">'+$(this).attr('loader-text')+'</h2></div>') ; 
       }
       $('#loader').slideDown();
       return true;
   });
    
   // Select All events 
   $('button[data-action=select_all]').click(function(e) {
   	    var $table = $('#'+$(this).attr('data-table')), $checkbox;
        
   	    if($($table.find('input[type=checkbox]').get(0)).is(':checked')) {
				$table.find('input[type=checkbox]').each(function() {
					var $t = $(this);
					$t.prop('checked', false);
					$t.closest($('tr')).removeClass('selected');
				});
   	    } else {
				$table.find('input[type=checkbox]').each(function() {
					var $t = $(this);
					$t.prop('checked', true);
					$t.closest($('tr')).addClass('selected');
				});
   	    }
        
        test_one_selected($table);
 			
   }); 
   
   
   // Select one event 
   $('table#maybe-table').find('input[type=checkbox]').each(function() {
        var $t = $(this);
        $t.click(function() {
            if($t.prop('checked')) {
                $t.closest($('tr')).addClass('selected');
            } else {
                $t.closest($('tr')).removeClass('selected');
            }
            test_one_selected($('table#maybe-table')); 
        });
        
         
   });
    
});