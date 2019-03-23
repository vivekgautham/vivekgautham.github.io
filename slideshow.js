
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
//getExif("photo" + slideIndex);

function plusSlides(n) {
  showSlides(slideIndex += n);
  //getExif("photo" + slideIndex);
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

function getExif(ide) {
    var img1 = document.getElementById(ide);
    EXIF.getData(img1, function() {
        var make = convertToFraction(EXIF.getTag(this, "ExposureTime"));
        var model = EXIF.getTag(this, "FNumber");
        var text = document.getElementById("text1");
        text.innerHTML = "Exposure Time " + `${make}`  + " secs, F-Stop " + `${model}`;
    });
}

function convertToFraction(x){
  function highestCommonFactor(a,b) {
    if (b==0) return a;
    return highestCommonFactor(b,a%b);
  }
  var decimalArray = x.toString().split(".");
  var leftDecimalPart = decimalArray[0];
  var rightDecimalPart = decimalArray[1];
  var numerator = leftDecimalPart + rightDecimalPart;
  var denominator = Math.pow(10,rightDecimalPart.length); 
  var factor = highestCommonFactor(numerator, denominator);
  denominator /= factor;
  numerator /= factor;
  return numerator + "/" + denominator;
}
/*
window.onload = function () {
  getExif("photo1");
};
*/