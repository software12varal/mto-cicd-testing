console.log("Create MTO");
$(document).ready(function() {
  $("#sign-up").submit(function(event) {
    event.preventDefault();
    $.ajax({
      data: $(this).serialize(),
      type: $(this).attr("method"),
      url: $(this).attr("action"),
      beforeSend: function() {
        $("#error-full-name").html("");
        $("#error-email").html("");
        $("#error-username").html("");
        $("#error-paypal-id").html("");
        $("#error-password1").html("");
        $("#error-password2").html("");
        $("#error-categories").html("");
        $("#error-contact").html("");
        $("#error-location").html("");
      },
      success: function(response) {
        console.log(response);
        if (response["redirect"]) {
          location.href = response["redirect"];
        }
        if (response["info"]) {
          iziToast.info({
            title: "Account Not Created:",
            message: response["info"],
            position: "topRight"
          });
        }
        if (response["full_name"]) {
          $("#error-full-name").html(response["full_name"]);
        }
        if (response["username"]) {
          $("#error-username").html(response["username"]);
        }
        if (response["email"]) {
          $("#error-email").html(response["email"]);
        }
        if (response["paypal_id"]) {
          $("#error-paypal-id").html(response["paypal_id"]);
        }
        if (response["password1"]) {
          $("#error-password1").html(response["password1"]);
        }
        if (response["password2"]) {
          $("#error-password2").html(response["password2"]);
        }
        if (response["job_category"]) {
          $("#error-categories").html(response["job_category"]);
        }
        if (response["contact_number"]) {
          $("#error-contact").html(response["contact_number"]);
        }
        if (response["location"]) {
          $("#error-location").html(response["location"]);
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
