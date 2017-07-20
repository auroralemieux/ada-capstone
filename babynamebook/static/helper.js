

$(document).ready(function() {
  $('#expand-all').on('click', function () {
    $('#accordion .panel-collapse').collapse('show');
  });

  $('#collapse-all').on('click', function () {
    $('#accordion .panel-collapse').collapse('hide');
  });

  // Getting a cookie by name
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = jQuery.trim(cookies[i]);
              // Does this cookie string begin with the name we want?
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }

  // Setup AJAX
  $(function () {
      $.ajaxSetup({
          headers: { "X-CSRFToken": getCookie("csrftoken") }
      });
  });

  // $(".name-group").on('mouseover', function() {
  //   var nameId = $(this).attr("data-id");
  //   var bookId = $(this).attr("data-book");
  //
  //   var whichHeart = "#heart" + nameId;
  //   $(whichHeart).show();
  //   function favoriteHandler(event) {
  //     if (event.handled !== true) {
  //       var toFavorite = function(nameId, bookId) {
  //         console.log(nameId);
  //         var book = bookId;
  //         var name = nameId;
  //
  //         $.ajax({
  //           url: "/favorite/",
  //           type: "POST",
  //           data: { 'name': name, 'book_id': book},
  //           success: function() {
  //             console.log("success!");
  //             var toggleHeart = function() {
  //               console.log("toggling heart");
  //               if ($(whichHeart).attr('src') == "../../static/plain-heart.jpg") {
  //                 $(whichHeart).attr("src", "../../static/blue-heart-icon.png");
  //               } else {
  //                 $(whichHeart).attr("src", "../../static/plain-heart.jpg");
  //               }
  //             };
  //             toggleHeart();
  //           }
  //         });
  //
  //         return false;
  //       };
  //
  //       toFavorite(nameId, bookId);
  //       event.handled = true;
  //     }
  //     return false;
  //   }
  //
  //   $(whichHeart).on('click', favoriteHandler);
  //
  // });

  // $(".fav-name").on('mouseover', function() {
  //   var nameId = $(this).attr("data-id");
  //   var whichGarbage = "#delete" + nameId;
  //   $(whichGarbage).show();
  //   function garbageHandler(event) {
  //     if (event.handled !== true) {
  //       var toGarbage = function(nameId) {
  //         console.log(nameId);
  //         var name = nameId;
  //
  //         $.ajax({
  //           url: "/garbage/",
  //           type: "POST",
  //           data: { 'name': name},
  //           success: function() {
  //             console.log("deleted from favorites!");
  //           }
  //         });
  //
  //         return false;
  //       };
  //
  //       toGarbage(nameId);
  //       event.handled = true;
  //     }
  //     return false;
  //   }
  //
  //   $(whichGarbage).on('click', garbageHandler);
  //
  // });
  //
  // $(".fav-name").on('mouseout', function() {
  //   var nameId = $(this).attr("data-id");
  //   var whichGarbage = "#delete" + nameId;
  //   $(whichGarbage).hide();
  // });

  //
  // $(".name-group").on('mouseout', function() {
  //   var nameId = $(this).attr("data-id");
  //   var whichHeart = "#heart" + nameId;
  //   if ($(whichHeart).attr('src') == "../../static/plain-heart.jpg") {
  //     $(whichHeart).hide();
  //   }
  // });


  var getSize = $('#id_tree_upload').change(function() {
    $(".filesize").hide();

    var file = this.files[0];
    var size = file.size;
    $(".filesize").html(size);
  });

  $('#upload-submit-button').on('click', function() {
    var size = $(".filesize").html();
    $('#percent').html('0%');
    var progressbar = $('#progressbar');
    var max = progressbar.attr('aria-valuemax');
    var time = size/10000;
    var value = progressbar.attr('aria-valuenow');

    var loading = function() {
      value = Number(value) + 1;
      progressbar.attr('aria-valuenow', value);
      newWidth = "width: " + value + "%";
      progressbar.attr('style', newWidth);
      $('#percent').html(value + '%');

      if (value == max) {
        clearInterval(animateProgress);
        $('#percent').html("finishing your book");
        $(".progress-bar").addClass("progress-bar-animated");
      }

    };
    var animateProgress = setInterval(function() {
      loading();
    }, time);

  animateProgress();
  });

});
