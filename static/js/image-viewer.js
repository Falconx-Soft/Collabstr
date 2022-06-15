function openModal(id) {
    get_images(id)
    document.getElementById("myModal").style.display = "block";
  }
  
  function closeModal() {
    document.getElementById("myModal").style.display = "none";
  }
  
  var slideIndex = 1;
  showSlides(slideIndex);
  
  function plusSlides(n) {
    showSlides(slideIndex += n);
  }
  
  function currentSlide(n) {
    showSlides(slideIndex = n);
  }
  
  function showSlides(n) {
    var i;
    var slides = document.getElementsByClassName("mySlides");
    var dots = document.getElementsByClassName("demo");
    var captionText = document.getElementById("caption");
    if (n > slides.length) {slideIndex = 1}
    if (n < 1) {slideIndex = slides.length}
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    for (i = 0; i < dots.length; i++) {
        dots[i].className = dots[i].className.replace(" active", "");
    }
    slides[slideIndex-1].style.display = "block";
    dots[slideIndex-1].className += " active";
    captionText.innerHTML = dots[slideIndex-1].alt;
  }

  function get_images(id) {
    var mydata = { id: id };
    $.ajax({
      url: "/get_images/",
      method: "GET",
      data: mydata,
      success: function (data) {

        let main_img = "";

        for(let i=0; i<data.length; i++){
            let count = i + 1 ;
            main_img += "<div class='mySlides'><div class='numbertext'>"+count+" / "+data.length+"</div><img src='"+data[i]+"' style='width:100%; height:80vh'></div>";
        }

        document.getElementById("main-image").innerHTML = main_img

        let img = "";

        for(let i=0; i<data.length; i++){
            let count = i + 1 ;
            img += "<div class='column'><img class='demo cursor' src='"+data[i]+"' style='width:100%; height: 100%;' onclick='currentSlide("+count+")' alt='Nature and sunrise'></div>";
        }

        document.getElementById("img-list").innerHTML = img
      },
    });
  }