$(document).ready(function(){
	$('[data-toggle="tooltip"]').tooltip();
});

function ShowImg(img_link, img_name) {
	$('#myModalImage').attr("src", img_link);
	$("#myModal").modal("show");
	document.getElementById("myModalLabel").innerHTML = img_name;
}