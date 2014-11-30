$(".document").click(function() {
  $("#summary_header").html($(this).html());
  $("#summary_authors").html($(this).next().html());
  $("#summary_authors > ul").dropotron();
  $('#summary').html('<p>Preparing summary</p>');
  request($(this).data("id"));
});

$( '#upload_form' )
  .submit( function( e ) {
    $.ajax( {
      url: 'http://localhost:5000/uploaded',
      type: 'POST',
      data: new FormData( this ),
      processData: false,
      contentType: false,
      success: function(data) {
        var t = $.parseJSON(data);
        $('#summary').html(t['text']);
      }
    } );
    e.preventDefault();
  });

function request(doc_id) {
    $.ajax({
      type: "POST",
      url: "http://localhost:5000/document",
      data: {
          'doc_id': doc_id
      },
      success: function(data) {
        var t = $.parseJSON(data);
        $('#summary').html(t['text']);
      }
  });
}