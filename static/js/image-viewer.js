//*************************************************** */ Slider
// Get the modal
var modal = document.getElementById("myModal00");

// Get the image and insert it inside the modal - use its "alt" text as a caption
const img = document.querySelectorAll("#myImg00");
const myImgDiv00 = document.querySelectorAll("#myImgDiv00");

var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption00");

const aplicaciones_slider_left_btn = document.getElementById(
  "aplicaciones-slider-left-btn"
);

const aplicaciones_slider_right_btn = document.getElementById(
  "aplicaciones-slider-right-btn"
);

let imagenumber = 0;
for (let i = 0; i < myImgDiv00.length; i++) {
  myImgDiv00[i].addEventListener("click", function () {
    imagenumber = i;
    modal.style.display = "block";
    modalImg.src = img[i].src;
    captionText.innerHTML = img[i].alt;
  });
}

// Get the <span> element that closes the modal
var span = document.getElementsByClassName("close00")[0];

// When the user clicks on <span> (x), close the modal
span.onclick = function () {
  modal.style.display = "none";
};

aplicaciones_slider_left_btn.addEventListener("click", function () {
  if (imagenumber == 0) {
    imagenumber = 3;
  }
  modalImg.src = img[imagenumber - 1].src;
  captionText.innerHTML = img[imagenumber - 1].alt;
  imagenumber--;
  console.log(imagenumber);
});

aplicaciones_slider_right_btn.addEventListener("click", function () {
  modalImg.src = img[imagenumber + 1].src;
  captionText.innerHTML = img[imagenumber + 1].alt;
  imagenumber++;
  if (imagenumber == 2) {
    imagenumber = -1;
  }
  console.log(imagenumber);
});
