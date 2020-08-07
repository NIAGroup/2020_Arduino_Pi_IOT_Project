function openSelection(evt, selectionName) {
  var i, x, tablinks;
  x = document.getElementsByClassName("selection");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < x.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" w3-border-red", "");
  }
  document.getElementById(selectionName).style.display = "block";
  evt.currentTarget.firstElementChild.className += " w3-border-red";
}

function closeMenu(menu_id_name){
document.getElementById(menu_id_name).style.display='none';
}