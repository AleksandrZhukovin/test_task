// Completing modal window to delete the pressed element
$(function(){
    $(document).on('click', '.delete-button', function(event){
        event.preventDefault();
        element = $(event.target);
        document.getElementById('submitMessage').innerHTML = `Are you sure you want to delete <b>${element.data('name')}</b>?`;
        button = $('#confirmDeletion');
        button.attr('hx-target', element.attr('hx-target'));
        button.attr('hx-headers', element.attr('hx-headers'));
        button.attr('hx-delete', element.data('url'));
        htmx.process(document.body);
    })
})