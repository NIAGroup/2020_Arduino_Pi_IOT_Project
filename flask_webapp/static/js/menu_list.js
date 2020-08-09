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