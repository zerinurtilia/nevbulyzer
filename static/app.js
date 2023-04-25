$(document).ready(function () {
  console.log("[INFO] script started");


  $("#button-input").click(function (e) {
    e.preventDefault();
    $("#button-input").addClass("hide");
    $("#button-reset").removeClass("hide");
    $("#result-loading").removeClass("hide");
    var text = $("#text-input").val();
    $.ajax({
      url: "/predict",
      type: "POST",
      data: JSON.stringify({ inputs: [text] }),

      contentType: "application/json",
      complete: function (data) {
        data.then((data) => {
          data = JSON.parse(data);
          $("#result-loading").addClass("hide");
          if (data[0] == 1) {
            $("#result-hate").removeClass("hide");
            $("#result-not-hate").addClass("hide");
          } else {
            $("#result-not-hate").removeClass("hide");
            $("#result-hate").addClass("hide");
          }
        });
      },
    });
  });

  $("#button-reset").click(function (e) {
    e.preventDefault();
    $("#button-reset").addClass("hide");
    $("#result-hate").addClass("hide");
    $("#result-not-hate").addClass("hide");
    $("#button-input").removeClass("hide");
    $("#text-input").val('');
  });
});

// Scroll top
var btn = $('#button');

$(window).scroll(function() {
  if ($(window).scrollTop() > 300) {
    btn.addClass('show');
  } else {
    btn.removeClass('show');
  }
});

btn.on('click', function(e) {
  e.preventDefault();
  $('html, body').animate({scrollTop:0}, '300');
});