$(".document").click(function() {
  request($(this).data("id"));
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