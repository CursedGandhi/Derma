var sec1img = ["images/img1.jpg","images/img2.jpg"];
var imgindex = 0;
function showsec1img(){
  var imageElement = document.getElementById("sec1-image");
  imageElement.src = sec1img[imgindex];
  setTimeout(function() {
    imageElement.src = images[currentIndex];
    imageElement.style.opacity = 1; // Set opacity to 1 to reveal the new image
}, 500);
}
function nextsec1img(){
  imgindex = (imgindex+1)% sec1img.length;
  showsec1img();
}
function prevsec1img(){
  imgindex = (imgindex-1 + sec1img.length) % sec1img.length;
  showsec1img();
}
function openDonate(){
  var donateURL = "donate.html";
  window.open(donateURL,'_blank')
}
/*function openindex(){
  var indexURL = "index.html";
  window.open(indexURL,'_blank');
}*/