$(document).ready(function() {

  $('#expand-all').on('click', function () {
    $('#accordion .panel-collapse').collapse('show');
  });

  $('#collapse-all').on('click', function () {
    $('#accordion .panel-collapse').collapse('hide');
  });



  $('#upload-submit-button').on('click', function() {
    $('#percent').html('0%');
    var progressbar = $('#progressbar');
    var max = progressbar.attr('aria-valuemax');
    var time = (5000/max*5);
    var value = progressbar.attr('aria-valuenow');

    var loading = function() {
      console.log();

      console.log("inside loading function");
      // newValue = value + 1;
      // console.log(newValue);
      value = Number(value) + 1;
      // addValue = progressbar.val(value);
      progressbar.attr('aria-valuenow', value);
      newWidth = "width: " + value + "%";
      progressbar.attr('style', newWidth);
      $('#percent').html(value + '%');

      if (value == max) {
        console.log("reached max");
        clearInterval(animateProgress);
        $(".progress-bar").addClass("progress-bar-animated");
      }

    };
    var animateProgress = setInterval(function() {
      console.log("inside animate Progress function");
      loading();
    }, time);

  animateProgress();
  });

});
