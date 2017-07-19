$(document).ready(function() {
  $('#expand-all').on('click', function () {
    $('#accordion .panel-collapse').collapse('show');
  });

  $('#collapse-all').on('click', function () {
    $('#accordion .panel-collapse').collapse('hide');
  });

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
