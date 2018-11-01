function booking() {
    $('#btnBook').click(function() {
 
        $.ajax({
            url: '/booking',
            data: $('form')[0].serialize(),
            type: 'POST',
            success: function(response) {
                console.log(response);
            },
            error: function(error) {
                console.log(error);
            }
        });
    });
}
