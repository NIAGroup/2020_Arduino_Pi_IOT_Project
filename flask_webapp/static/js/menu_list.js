function openSelection(evt, selectionName) {
  closeMenu();
  document.getElementById(selectionName).style.display = "block";
  evt.currentTarget.firstElementChild.className += " w3-border-red";
}

function closeMenu(){
  var i, x, tablinks;
  x = document.getElementsByClassName("selection");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < x.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" w3-border-red", "");
  }
}

function changeRunButtonColor(){
  var btn;
  btn = document.getElementById("runBtn");
  
  if(btn.classList.contains("btn-success"))
  {
    btn.classList.remove("btn-success");
    btn.classList.add("btn-danger")
  }
  else if (btn.classList.contains("btn-danger"))
  {
    btn.classList.remove("btn-danger");
    btn.classList.remove("btn-success");
  }
  else
  {
    btn.classList.add("btn-success");
  }
  
}

function changeConnectButtonColor(){
  var btn;
  btn = document.getElementById("connectBtn");
  
  if(btn.classList.contains("btn-success"))
  {
    btn.classList.remove("btn-success");
    btn.classList.add("btn-danger")
  }
  else if (btn.classList.contains("btn-danger"))
  {
    btn.classList.remove("btn-danger");
    btn.classList.remove("btn-success");
  }
  else
  {
    btn.classList.add("btn-success");
  }
  
}

function thumbnailSelect(){
  var btnContainer;
  btnContainer = document.getElementById("thumbnailBtn");
  
  var btns;
  btns = btnContainer.getElementsByClassName("thumbnail");
  
  // Loop through the buttons and add the active class to the current/clicked button
  for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener("click", function() {
      var current = document.getElementsByClassName("active");

      // If there's no active class
      if (current.length > 0) {
        current[0].className = current[0].className.replace(" active", "");
      }

      // Add the active class to the current/clicked button
      this.className += " active";
    });
	}
}