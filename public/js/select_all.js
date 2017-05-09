
function delete_all() {
    var events = [];
    var url = window.location.pathname+'/delete_multiple';
    var form;
    
    $('button[data-action=delete-all]').click(function() {
        $('.select-events-table input[type=checkbox]:checked').each(function() {
            events.push($(this).attr('name')); 
        });
        
        form = $('<form action="' + url + '" method="post">' +
          '<input type="text" name="events" value="' + events + '" />' +
          '</form>');
        $('body').append(form);
        form.submit();
      });
}

$(function() {
    
        
    delete_all();         
    
})