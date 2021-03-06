console.log("updated adding mal requirements ");
const uploadForm = document.getElementById("add-mal-form");
const input = document.getElementById("id_job_sample");
console.log(input);
const csrf = document.getElementsByName("csrfmiddlewaretoken");
const identification_number = document.getElementById(
  "id_identification_number"
);
const assembly_line_id = document.getElementById("id_assembly_line_id");
const assembly_line_name = document.getElementById("id_assembly_line_name");
const person_name = document.getElementById("id_person_name");
const output = document.getElementById("id_output");
const job_name = document.getElementById("id_job_name");
const cat_id = document.getElementById("id_cat_id");
const target_date = document.getElementById("id_target_date");
const total_budget = document.getElementById("id_total_budget");
const job_description = document.getElementById("id_job_description");
const job_instructions = document.getElementById("id_job_instructions");
const job_quantity = document.getElementById("id_job_quantity");
const input_folder = document.getElementById("id_input_folder");
$(document).ready(function(){
  $("#id_cat_id").click(function(){
    $("p").prepend("<b>Prepended text</b>. ");
  });
});


uploadForm.addEventListener("submit", e => {
  e.preventDefault();

  const fd = new FormData();
  
  const sample_data = $('#id_sample').files
  const instructions_data = $('#id_instructions').files

  fd.append("csrfmiddlewaretoken", csrf[0].value);
  fd.append("identification_number", identification_number.value);
  fd.append("assembly_line_id", assembly_line_id.value);
  fd.append("assembly_line_name", assembly_line_name.value);
  fd.append("person_name", person_name.value);
  fd.append("output", output.value);
  fd.append("job_name", job_name.value);
  fd.append("cat_id", cat_id.value);
  fd.append("target_date", target_date.value);
  fd.append("total_budget", total_budget.value);
  fd.append("job_description", job_description.value);
  fd.append("job_quantity", job_quantity.value);
  fd.append("input_folder", input_folder.value);
  fd.append('sample',sample_data )
  fd.append('instructions',instructions_data )
  

  $.ajax({
    type: "POST",
    url: uploadForm.action,
    enctype: "multipart/form-data",
    data: fd,
    beforeSend: function() {
      $("#error-identification-number").html("");
      $("#error-assembly-line-id").html("");
      $("#error-assembly-line-name").html("");
      $("#error-person-name").html("");
      $("#error-output").html("");
      $("#error-micro-task").html("");
      $("#error-micro-task-category").html("");
      $("#error-target-date").html("");
      $("#error-total-budget").html("");
      $("#error-job-description").html("");
      // $("#error-job-sample").html("");
      // $("#error-job-instructions").html("");
      $("#error-job-quantity").html("");
      $("#error-input-folder").html("");
    },
    success: function(response) {
      console.log(response);
      if (response["message"]) {
        $("#message").html(response["message"]);
        $(window).scrollTop(0);
      }
      if (response["identification_number"]) {
        $("#error-identification-number").html(
          response["identification_number"]
        );
      }
      if (response["assembly_line_id"]) {
        $("#error-assembly-line-id").html(response["assembly_line_id"]);
      }
      if (response["assembly_line_name"]) {
        $("#error-assembly-line-name").html(response["assembly_line_name"]);
      }
      if (response["person_name"]) {
        $("#error-person-name").html(response["person_name"]);
      }
      if (response["output"]) {
        $("#error-output").html(response["output"]);
      }
      if (response["job_name"]) {
        $("#error-micro-task").html(response["job_name"]);
      }
      if (response["cat_id"]) {
        $("#error-micro-task-category").html(response["cat_id"]);
      }
      if (response["target_date"]) {
        $("#error-target-date").html(response["target_date"]);
      }
      if (response["total_budget"]) {
        $("#error-total-budget").html(response["total_budget"]);
      }
      if (response["job_description"]) {
        $("#error-job-description").html(response["job_description"]);
      }
      // if (response["job_sample"]) {
      //   $("#error-job-sample").html(response["job_sample"]);
      // }
      // if (response["job_instructions"]) {
      //   $("#error-job-instructions").html(response["job_instructions"]);
      // }
      if (response["job_quantity"]) {
        $("#error-job-quantity").html(response["job_quantity"]);
      }
      if (response["input_folder"]) {
        $("#error-input-folder").html(response["input_folder"]);
      }
    },
    error: function(error) {
      console.log(error);
      iziToast.error({
        title: error.status,
        message: error.statusText,
        position: 'topRight'
      });
    },
    cache: false,
    contentType: false,
    processData: false
  });
});

