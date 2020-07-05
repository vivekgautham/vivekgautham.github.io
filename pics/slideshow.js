
var arrayDiv;

for(var i=1; i <= 12; i++){
  arrayDiv = document.createElement('div');
  arrayDiv.id = 'mySlides fade' + i;
  arrayDiv.className = 'mySlides fade';
  elem = document.createElement('img');
  elem.setAttribute("src", "https://github.com/vivekgautham/vivekgautham.github.io/blob/master/mygraphic/" + i + ".JPG?raw=true");
  elem.setAttribute("width", "1000");
  elem.setAttribute("id", "photo" + i);
  arrayDiv.appendChild(elem);
  document.getElementById("slide1").appendChild(arrayDiv);
}
elem = document.createElement('a');
elem.className = "prev";
elem.setAttribute("onclick", "plusSlides(-1)");
elem.innerHTML = "&#10094;"
document.getElementById("slide1").appendChild(elem);

elem = document.createElement('a');
elem.className = "next";
elem.setAttribute("onclick", "plusSlides(1)");
elem.innerHTML = "&#10095;"
document.getElementById("slide1").appendChild(elem);

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
  var texts = document.getElementsByClassName("text");
  if (n > slides.length) {slideIndex = 1}
  if (n < 1) {slideIndex = slides.length}
  for (i = 0; i < slides.length; i++) {
      slides[i].style.display = "none";
  }
  slides[slideIndex-1].style.display = "block";
}
