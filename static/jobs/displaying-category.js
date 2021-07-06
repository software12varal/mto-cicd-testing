$(document).ready(function(){
   $("#id_cat_id").click(function(){
     console.log("Displaying category.")
       var id = this.value
       console.log(id)
         getCategories(id)
   });
 });
 
 function getCategories(id){
        console.log('getting data....')
       fetch(get_cat_url, {
          method:'POST',
          headers:{
             'Content-Type':'application/json',
             'X-CSRFToken':csrftoken,
          },
          body:JSON.stringify({'cat_id':id})
       })
       .then((response) => {
           console.log(response)
           if (response['statusText'] != 'OK'){
           iziToast.error({
               title: response['status'],
               message: response['statusText'],
               position: 'topRight'
             });
             }
          return response.json();
       })
       .then((data) => {
           console.log(data)
           if (data['message']){
                 iziToast.success({
                   title: 'Displaying category:',
                   message: data['message'],
                   position: 'topRight'
                 });
           }
           if (data.sample != undefined ){
               $('#jobs-category').html(`<b>Existing Job Sample:</b><a href="${data.sample}">${data.sample}</a>
               <input name="sample" id="id_sample" type="file" value='${data.sample}' class="form-control"><br/>
               <b>Existing Job Instructions:</b><a href="${data.instructions}">${data.instructions}</a>
               <input name="instructions" id="id_instructions" type="file" value='${data.instructions}' class="form-control">
               <br/>
               `)
           }
       });
 }