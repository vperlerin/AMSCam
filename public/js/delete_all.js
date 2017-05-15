
function delete_all() {
    var events = [];
    var url = window.location.pathname+'/delete_multiple';
    var form;
    
    $('button[data-action=delete-all]').click(function(e) {
         e.stopPropagation();
         
         bootbox.confirm({
            message: 'You are about to permanently remove these ' + $('.select-events-table input[type=checkbox]:checked').length + ' events. Please, confirm.',
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
                     $('.select-events-table input[type=checkbox]:checked').each(function() {
                        events.push($(this).attr('name')); 
                    });
                    
                    form = $('<form action="' + url + '" method="post">' +
                      '<input type="text" name="events" value="' + events + '" />' +
                      '</form>');
                    $('body').append(form);
                    form.submit();
                }
            }
        });   
        
        return false;
        
       
      });
}

$(function() {
    delete_all();         
})