var dropdown = document.getElementById("myDropdown");
var mainContainer = document.getElementById("container");
var isRotated = false; 

function dropdownMenu() {
    dropdown.classList.toggle("show");

    var button = document.querySelector('.dropbtn');
    isRotated = !isRotated;
    button.classList.toggle("rotate", isRotated);

    if (dropdown.classList.contains('show')) {
        var additionalMargin = 50; // Adjust this value as needed
        mainContainer.style.marginTop = (dropdown.offsetHeight + button.offsetHeight + additionalMargin) + 'px';
    } else {
        mainContainer.style.marginTop = '';
    }
}


window.onclick = function(event) {
  if (!event.target.matches('.dropbtn')) {
    var dropdowns = document.getElementsByClassName("dropdown-content");
    for (var i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i];
      if (openDropdown.classList.contains('show')) {
        openDropdown.classList.remove('show');
      }
    }

    var button = document.querySelector('.dropbtn');
    if (isRotated) {
      isRotated = false;
      button.classList.remove("rotate");
    }

    mainContainer.style.marginTop = '';
  }
}

