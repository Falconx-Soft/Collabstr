function myFunction() {
    var input, filter, table, tr, td, i, txtValue;
    input = document.getElementById("myInput");
    filter = input.value.toUpperCase();
    table = document.getElementById("myTable");
    tr = table.getElementsByTagName("tr");
    for (i = 0; i < tr.length; i++) {
      td = tr[i].getElementsByTagName("td")[0];
      if (td) {
        txtValue = td.textContent || td.innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }       
    }
  }

  function sortTable() {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("myTable");
    switching = true;
    /*Make a loop that will continue until
    no switching has been done:*/
    while (switching) {
      //start by saying: no switching is done:
      switching = false;
      rows = table.rows;
      /*Loop through all table rows (except the
      first, which contains table headers):*/
      for (i = 1; i < (rows.length - 1); i++) {
        //start by saying there should be no switching:
        shouldSwitch = false;
        /*Get the two elements you want to compare,
        one from current row and one from the next:*/
        x = rows[i].getElementsByTagName("TD")[0];
        y = rows[i + 1].getElementsByTagName("TD")[0];
        //check if the two rows should switch place:
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
      if (shouldSwitch) {
        /*If a switch has been marked, make the switch
        and mark that a switch has been done:*/
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
      }
    }
  }

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


// search bar
