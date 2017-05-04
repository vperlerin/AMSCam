$(function() {
    
   $('.load-on-click').click(function(e) {
       $(this).html('<span class="fa fa-spinner fa-spin"></span>');
       return true;
   });
    
});