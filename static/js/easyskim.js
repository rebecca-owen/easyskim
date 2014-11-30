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
        var meta = $.parseJSON(t['meta']);
        $("#summary_header").html('<strong>' + meta['Title'] + '</strong>');
        $("#summary_authors").html(prettyAuthors(meta['Author']));
        $("#summary_authors > ul").dropotron();
      }
    } );
    e.preventDefault();
  });

function prettyAuthors(authors) {

  console.log(authors)
  authors = authors.split(';');
  console.log(authors)

  if(authors.length > 2) {
    first_two = authors[0] + '; ' + authors[1];
    html = '<ul class="dropdown"><li>' + first_two + '; et al.<ul>';
    for(i=0; i < authors.length - 2; i++) {
      html += '<li>' + authors[i+2] + '<li>';      
    }
    html += '</ul></li></ul>'   
  }

  else{
    if(authors.length == 2){
      temp = authors[0] + ', ' + authors[1]
    }
    else if (authors.length == 1){
      temp = authors[0]
    }
    else if (authors.length == 0){
      temp = 'Not Available'
    }
    html = '<p>' + temp + '</p>'
  }

  return html
}

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