// overide default submit action to specifiy what to do with res




function onFileSelected(event) {
  var selectedFile = event.target.files[0];
  var reader = new FileReader();

  var imgtag = document.getElementById("currentImage");
  imgtag.title = selectedFile.name;

  reader.onload = function(event) {
    imgtag.src = event.target.result;
  };
  reader.readAsDataURL(selectedFile);
};


$(document).ready(function(){
	$("form").submit(function(event) {
		event.preventDefault() // so that form doesn't try to complete post
        var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/upload',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: false,
            success: function(result,status) {
				res = JSON.parse(result)
				//alert(res['sentiment'])
				$("#submit_button").attr({"value":"changed"});
            },
        });
	});
});	





