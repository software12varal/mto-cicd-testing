console.log("Verifying Email");
$(document).ready(function() {
  $("#email-verification").submit(function(event) {
    event.preventDefault();
    $.ajax({
      data: $(this).serialize(),
      type: $(this).attr("method"),
      url: $(this).attr("action"),
      beforeSend: function() {
        $("#error-otp").html("");
      },
      success: function(response) {
        console.log(response);
        if(response['message']) {
         iziToast.success({
            title: 'Email Verified:',
            message: response['message'],
            position: 'topRight'
          });
         setTimeout(function () {
         location.href = response['redirect']
        }, 5200);
        }
        if (response["info"]) {
          iziToast.info({
            title: "Not Verified:",
            message: response["info"],
            position: "topRight"
          });
        }
        if (response["otp"]) {
          $("#error-otp").html(response["otp"]);
        }
      },
      error: function(request, status, error) {
        console.log(request.responseText);
        iziToast.error({
          title: status,
          message: error,
          position: "topRight"
        });
      }
    });
  });
});
