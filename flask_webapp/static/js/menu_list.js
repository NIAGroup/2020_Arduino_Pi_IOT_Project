/**
 * @file   This file is specific to the PID IOT project. It defines th functionality of drop-down menus.
 * @author Adonay Berhe, Felicia James
 * @since  10.14.2020
 */

function openSelection(evt, selectionName) {
  if (document.getElementById(selectionName).style.display === "block"){
    closeMenu();
    return;
  }
  else{
    closeMenu();
    document.getElementById(selectionName).style.display = "block";
    evt.currentTarget.firstElementChild.className += "w3-border-red";
    if (selectionName === "Scan"){
      // Clear the row of previously scanned device image columns
      clearChildNodes("scan_device_row");

      // Perform a scan and grab data from back-end
      var url = "/scan";
      d3.json(url, {method: "GET", headers: {"Content-type": "application/json; charset=UTF-8"}}).then((data_in)=>{
        if (data_in === null || data_in.scan_devs === undefined || data_in.scan_devs.length == 0) {
          drawNoDeviceMessage();
        }
        else{
          data_in.scan_devs.forEach(drawDevices);
        }
      });
    }
  }
}

function clearChildNodes(elt_id){
  var scan_dev_row = document.getElementById(elt_id);
  scan_dev_row.querySelectorAll('*').forEach(n => n.remove());
}

function drawNoDeviceMessage(elt_id){
  var no_dev_text = document.createTextNode("Couldn't find any bluetooth devices.");

  var dev_header = document.createElement("h6");
  dev_header.style = "text-align:center; padding-top:15px";
  dev_header.appendChild(no_dev_text);

  var dev_column = document.createElement("div");
  dev_column.setAttribute("class", "col");
  dev_column.appendChild(dev_header);
  if (elt_id === "Scan")
  {
  var scan_dev_row = document.getElementById("Scan");
  scan_dev_row.appendChild(dev_column);
  }
  
  if (elt_id === "ScanDB")
  {
  var scanDB_dev_row = document.getElementById("ScanDB");
  scanDB_dev_row.appendChild(dev_column);
  }
}

function drawDevices(name, index){
  var dev_image = document.createElement("img");
  dev_image.setAttribute("src", "../static/img/arduino_icon_transparent.jpg");
  dev_image.setAttribute("alt", "Arduino icon");

  var dev_a_tag = document.createElement("a");
  dev_a_tag.setAttribute("class", "thumbnail");
  dev_a_tag.setAttribute("onclick", "thumbnailSelect(this)");
  dev_a_tag.appendChild(dev_image);

  var dev_paragraph = document.createElement("p");
  dev_paragraph.setAttribute("style", "text-align:center");
  var dev_name_text = document.createTextNode(name);
  dev_paragraph.appendChild(dev_name_text);

  var dev_column = document.createElement("div");
  dev_column.classList = "col scanDev";
  dev_column.id = name;
  dev_column.appendChild(dev_a_tag);
  dev_column.appendChild(dev_paragraph);

  var scan_dev_row = document.getElementById("Scan");
  scan_dev_row.appendChild(dev_column);

}
function drawScanDBDevices(name, index){
  var dev_image = document.createElement("img");
  dev_image.setAttribute("src", "../static/img/arduino_icon_transparent.jpg");
  dev_image.setAttribute("alt", "Arduino icon");

  var dev_a_tag = document.createElement("a");
  dev_a_tag.setAttribute("class", "thumbnail");
  dev_a_tag.setAttribute("onclick", "thumbnailSelect(this)");
  dev_a_tag.appendChild(dev_image);

  var dev_paragraph = document.createElement("p");
  dev_paragraph.setAttribute("style", "text-align:center");
  var dev_name_text = document.createTextNode(name);
  dev_paragraph.appendChild(dev_name_text);

  var dev_column = document.createElement("div");
  dev_column.classList = "col scanDev";
  dev_column.id = name;
  dev_column.appendChild(dev_a_tag);
  dev_column.appendChild(dev_paragraph);

  var scan_dev_row = document.getElementById("ScanDB");
  scan_dev_row.appendChild(dev_column);

}

function closeMenu(){
  var i, x; 
  /* var tablinks; */
  x = document.getElementsByClassName("selection");
  for (i = 0; i < x.length; i++) {
    x[i].style.display = "none";
  }
/*   tablinks = document.getElementsByClassName("tablink");
  for (i = 0; i < x.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" w3-border-red", "");
  } */
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

function getSelectedDevices(){
  var devices = document.getElementsByClassName("scanDev");
  var selectedDevices = {};
  for (device of devices)
  {
    devChilda = device.getElementsByTagName('a')[0];
    devChildp = device.getElementsByTagName('p')[0];
    if (devChilda.classList.contains('active'))
    {
      selectedDevices[devChildp.innerHTML] = [devChilda, devChildp];
    }
  }

  return selectedDevices;
}
function triggerConnection(connectBtn){
  var deviceNames = {};
  var selectedDevices = getSelectedDevices();
  if($.isEmptyObject(selectedDevices))
  {
    return;
  }

  deviceNames["selectedDevices"]  = Object.keys(selectedDevices);
  var isConnected = false;
  var url = "/connect";
  d3.json(url, {method: "POST", body: JSON.stringify(deviceNames),
    headers: {"Content-type": "application/json; charset=UTF-8"}}).then((returnVal)=>{
    var error = "";

    Object.entries(returnVal).forEach(([devName, connectionStatus]) => {
      if(connectionStatus === true && deviceNames["selectedDevices"].includes(devName))
      {
        selectedDevices[devName][0].classList.toggle("active");
        selectedDevices[devName][0].classList.add("connected");
        isConnected = true;
      }
      else
      {
        error = error.concat(devName, " ");
      }
    })
    console.log(error.length);
    if (error.length > 0)
    {
      alert("These devices were not able to connect. Check server logs [log location here...] for details.\n".concat(error));
    }
    if(isConnected)
    {
      connectBtn.classList.add("btn-success");
    }
  });
}


function thumbnailSelect(element){
  
  $('.scanDev a.active').removeClass('active') /* select one thumbnail at a time */ 
  element.classList.toggle("active");
}


function scanBTDevice(evt, selectionName) {
  if (document.getElementById(selectionName).style.display === "flex"){
    closeMenu();
    return;
  }
  if (document.getElementById("ScanDB").style.display === "flex"){
    closeMenu();
    return;
  }
  else{
    closeMenu();
	document.getElementById(selectionName).style.display = "flex";
	document.getElementById(selectionName).style.flexWrap = "wrap";
	document.getElementById("ScanDB").style.display = "flex";
	document.getElementById("ScanDB").style.flexWrap = "wrap";
    //evt.currentTarget.firstElementChild.className += "w3-border-red";
     if (selectionName === "Scan"){
      // Clear the row of previously scanned device image columns

	  clearChildNodes("ScanDB")
	  var scanDBurl= "/previously_paired";
	  d3.json(scanDBurl, {method: "GET", headers: {"Content-type": "application/json; charset=UTF-8"}}).then((data_in)=>{
        if (data_in === null || data_in.prev_devs === undefined || data_in.prev_devs.length == 0) {
          setTimeout(function(){drawNoDeviceMessage("ScanDB");},2000);
        }
        else{
          setTimeout(function(){data_in.prev_devs.forEach(drawScanDBDevices);},2000);
        }
      });
	  
      setTimeout(function(){clearChildNodes("Scan");},2000);
     // Perform a scan and grab data from back-end
      var scanurl = "/scan";
      d3.json(scanurl, {method: "GET", headers: {"Content-type": "application/json; charset=UTF-8"}}).then((data_in)=>{
        if (data_in === null || data_in.scan_devs === undefined || data_in.scan_devs.length == 0) {
          setTimeout(function(){drawNoDeviceMessage("Scan");},2000);
        }
        else{
          setTimeout(function(){data_in.scan_devs.forEach(drawDevices);},2000);
        }
      });
    } 
  }
}



/* function streamVideo(){
	
	$('#stream_video').attr('style', "width:100%;height:100%");
	clearChildNodes("videofeed_col");
	var loading_text = document.createTextNode("Loading video feed...");
	var vf_header = document.createElement("h6");
	vf_header.appendChild(loading_text);
	var vf_row = document.getElementById("videofeed_col");
	vf_row.appendChild(vf_header);

	var vf1_spinner = document.createElement("div");
	vf1_spinner.setAttribute("class", "spinner-grow spinner-grow-sm text-primary");
	vf1_spinner.setAttribute("animation", "spinner-grow 1.10s ease-in-out 0.2s infinite;");
	vf1_spinner.setAttribute("role", "status");

	var vf2_spinner = document.createElement("div");
	vf2_spinner.setAttribute("class", "spinner-grow spinner-grow-sm text-primary");
	vf2_spinner.setAttribute("animation", "spinner-grow 1.10s ease-in-out 0.4s infinite;");
	vf2_spinner.setAttribute("role", "status");

	var vf3_spinner = document.createElement("div");
	vf3_spinner.setAttribute("class", "spinner-grow spinner-grow-sm text-primary");
	vf3_spinner.setAttribute("animation", "spinner-grow 1.10s ease-in-out 0.6s infinite;");
	vf3_spinner.setAttribute("role", "status");

	vf_row.appendChild(vf1_spinner);
	vf_row.appendChild(vf2_spinner);
	vf_row.appendChild(vf3_spinner);

	clearChildNodes("videofeed_col");

	var vf_img = document.createElement("img");
	vf_img.setAttribute("style", "width:100%;height:100%");
	vf_img.setAttribute("src", "{{ url_for('video_feed') }}");
	vf_row.appendChild(vf_img);

}; */
