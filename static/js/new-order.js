$(document).ready(function(){
	  
	let table = new DataTable('#example', {
        scrollY: 300,
        paging: false,
        "searching": false
    });

  $('#search-order').on('keydown', function(){
    console.log("Pressed",this.value);
      table
        .columns( 1 )
        .search( this.value )
        .draw();
  });	

  $('.nav-tabs a[href="#public"]').tab('show');
	$('.nav-tabs a[href="#systematic_trading"]').tab('show');

});	

requests_btn = document.getElementById("requests_btn");
in_progress_btn = document.getElementById("in_progress_btn");
completed_btn = document.getElementById("completed_btn");

requests_div = document.getElementById("requests_div");
in_progress_div = document.getElementById("in_progress_div");
completed_div = document.getElementById("completed_div");

requests_btn.addEventListener("click", function(){
    in_active();
    requests_div.style.display = "block";
    requests_btn.classList.add('active');
});


in_progress_btn.addEventListener("click", function(){
    in_active();
    in_progress_div.style.display = "block";
    in_progress_btn.classList.add('active');
});

completed_btn.addEventListener("click", function(){
    in_active();
    in_progress_div.style.display = "block";
    completed_btn.classList.add('active');
});

function in_active(){
    requests_btn.classList.remove('active');
    in_progress_btn.classList.remove('active');
    completed_btn.classList.remove('active');

    requests_div.style.display = "none";
    in_progress_div.style.display = "none";
    in_progress_div.style.display = "none";
}