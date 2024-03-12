$(function(){
    $('#addToDoListBtn').click(function(){
        document.getElementById('main').inert = true;
        document.getElementById('addToDoList').show();
        document.getElementById('addToDoList').classList.add('dialog_appear');
    })
})

$(function(){
    $('#closeAddToDoList').click(function(){
        document.getElementById('main').inert = false;
        document.getElementById('addToDoList').close();
        document.getElementById('addToDoList').classList.remove('dialog_appear');
    })
})

$(function(){
    $('#sendToDoList').click(function(){
        $.ajax('/add_to_do_list/', {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val(),
                'name': $('#projectName').val()
            },
            'success': function(data){
                if (document.getElementById('message')) {
                    document.getElementById('message').remove();
                }
                document.getElementById('projects').innerHTML = data + document.getElementById('projects').innerHTML;
                document.getElementById('main').inert = false;
                document.getElementById('addToDoList').close();
                $('#projectName').val('');
                htmx.process(document.body);
            }
        })
    })
})