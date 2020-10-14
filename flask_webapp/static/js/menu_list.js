function openSelection(evt, selectionName) {
  closeMenu();
  document.getElementById(selectionName).style.display = "block";
  evt.currentTarget.firstElementChild.className += "w3-border-red";
  if (selectionName === "Scan"){
    // Clear the row of previously scanned device images
    clearScanDeviceRow();

    // Perform a scan and grab data from back-end
    var url = "/scan";
    d3.json(url).then((data_in) => {

      if (data_in === null || data_in.scan_devs === undefined || data_in.scan_devs.length == 0) {
        drawNoDeviceMessage();
      }
      else{
        data_in.scan_devs.forEach(drawDevices);
      }
    });
  }
}

function clearScanDeviceRow()
{
  var scan_dev_row = document.getElementById("scan_device_row");
  scan_dev_row.querySelectorAll('*').forEach(n => n.remove());
}

function drawNoDeviceMessage(){
  var no_dev_text = document.createTextNode("Couldn't Find any bluetooth devices.");
  var dev_header = document.createElement("h6");
  dev_header.appendChild(no_dev_text);
  var scan_dev_row = document.getElementById("scan_device_row");
  scan_dev_row.appendChild(dev_header);
}

function drawDevices(name, index){
  var dev_image = document.createElement("img");
  dev_image.src = "../static/img/arduino_icon_transparent.jpg";
  //dev_image.setAttribute("src", "static\img\arduino_icon_transparent.jpg");
  dev_image.setAttribute("alt", "Arduino icon");

  var dev_a_tag = document.createElement("a");
  dev_a_tag.setAttribute("class", "thumbnail");
  dev_a_tag.setAttribute("onclick", "thumbnailSelect()");
  dev_a_tag.appendChild(dev_image);

  var dev_paragraph = document.createElement("p");
  dev_paragraph.setAttribute("style", "text-align:center;");
  var dev_name_text = document.createTextNode(name);
  dev_paragraph.appendChild(dev_name_text);

  var dev_column = document.createElement("div");
  dev_column.setAttribute("class", "col");
  dev_column.appendChild(dev_a_tag);
  dev_column.appendChild(dev_paragraph);

  var scan_dev_row = document.getElementById("scan_device_row");
  scan_dev_row.appendChild(dev_column);
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