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
	$("form").submit(function() {
        var form_data = new FormData($('#upload-file')[0]);
        $.ajax({
            type: 'POST',
            url: '/upload',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: false,
            success: function(result) {
				var ctx = document.getElementById("result").getContext("2d");
				res = JSON.parse(result)
				var data = {
					labels: res['sentiment'],
					datasets: [
						{
							label: "Face Analysis",
							fillColor: "white",
							data: res['score']
						}
					]
				};
				var myLineChart = new Chart(ctx).Bar(data, {
					showScale: false
				});
                
            },
        });
	return false; // so that form doesn't try to complete post
	});
});	





