/**
 * @file   This file is specific to the PID IOT project. It defines the functionality of drop-down menus.
 * @author Adonay Berhe, Felicia James
 * @since  10.14.2020
 */
/*
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
*/

var baseUrl = "";
var HTTP_200_OK = 200;
var HTTP_201_CREATED = 201;
var HTTP_202_ACCEPTED = 202;
var HTTP_204_NO_CONTENT = 204;
var HTTP_404_NOT_FOUND = 404;
var HTTP_512_DOUBLE_ENTRY_DB_ERROR = 512;
var HTTP_515_NO_DEVICE_RETURNED = 515;

function getPreviouslyPairedDevices(){
    var html_elt_id_name = "PreviousPaired";
    var prev_paired_row = document.getElementById(html_elt_id_name);
    prev_paired_row.style.display = "flex";
	prev_paired_row.style.flexWrap = "wrap";

	clearChildNodes(html_elt_id_name);
    var url= baseUrl.concat("/get_previously_paired");
    fetch(url, {
        method: "GET",
        headers: {"Content-type": "application/json; charset=UTF-8"},
    })
    .then(response => {
        if (response.status === HTTP_200_OK){
            return  response.json();
        }
        else if (response.status === HTTP_404_NOT_FOUND){
            setTimeout(function(){drawNoDeviceMessage(html_elt_id_name);},2000);
            throw new Error("No previously connected devices. \n" + response.status + ": " + response.statusText);
        }
        else {
            setTimeout(function(){drawNoDeviceMessage(html_elt_id_name);},2000);
            throw new Error("An unexpected error occurred. \n" + response.status + ": " + response.statusText);
        }
    })
    .then(data => {
        setTimeout(function(){data.previously_paired_devices.forEach(drawPreviouslyPairedDevices);},2000);
    })
    .catch(err => console.error(err));
}

function getScanDevices() {
    var html_elt_id_name = "Scan";
    var scan_row = document.getElementById(html_elt_id_name);
    clearChildNodes(html_elt_id_name);
    scan_row.style.display = "flex";
    scan_row.style.flexWrap = "wrap";

    var url= baseUrl.concat("/scan");
    fetch(url, {
        method: "GET",
        headers: {"Content-type": "application/json; charset=UTF-8"},
    })
    .then(response => {
        if (response.status === HTTP_200_OK){
            return  response.json();
        }
        else if (response.status === HTTP_404_NOT_FOUND){
            setTimeout(function(){drawNoDeviceMessage(html_elt_id_name);},2000);
            throw new Error("No devices available.\n" + response.status + ": " + response.statusText);
        }
        else {
            setTimeout(function(){drawNoDeviceMessage(html_elt_id_name);},2000);
            throw new Error("An unexpected error occurred. \n" + response.status + ": " + response.statusText);
        }
    })
    .then(data => {
        data.scanned_devices.forEach(drawScannedDevices);
    })
    .catch(err => console.error(err));
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
  
  if (elt_id === "PreviousPaired")
  {
  var scanDB_dev_row = document.getElementById("PreviousPaired");
  scanDB_dev_row.appendChild(dev_column);
  }
}

function drawDevicesInRows(device, index, rowName){
  var dev_image = document.createElement("img");
  dev_image.setAttribute("src", "../static/img/arduino_icon_transparent.jpg");
  dev_image.setAttribute("alt", "Arduino icon");

  var dev_a_tag = document.createElement("a");
  dev_a_tag.setAttribute("class", "thumbnail");
  if (device.status === "connected"){
    dev_a_tag.setAttribute("style", "border-color : green", "border-width : thick");
  }
  dev_a_tag.setAttribute("onclick", "thumbnailSelect(this)");
  dev_a_tag.appendChild(dev_image);

  var dev_paragraph = document.createElement("p");
  dev_paragraph.setAttribute("style", "text-align:center");
  var dev_name_text = document.createTextNode(device.name);
  dev_paragraph.appendChild(dev_name_text);

  var dev_column = document.createElement("div");
  dev_column.classList = "col scanDev";     // This class name needs to change
  dev_column.id = device.name;
  dev_column.appendChild(dev_a_tag);
  dev_column.appendChild(dev_paragraph);

  var scan_dev_row = document.getElementById(rowName);
  scan_dev_row.appendChild(dev_column);
}

function drawScannedDevices(name, index){
  drawDevicesInRows(name, index, "Scan");
}

function drawPreviouslyPairedDevices(device, index){
  drawDevicesInRows(device, index, "PreviousPaired");
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

  var url= baseUrl.concat("/connect");
    fetch(url, {
        method: "POST",
        headers: {"Content-type": "application/json; charset=UTF-8"},
        body: JSON.stringify(deviceNames)
    })
    .then(response => {
        if ((response.status === HTTP_201_CREATED) or (response.status === HTTP_202_ACCEPTED)){
            return  response.json();
        }
        else if (response.status === HTTP_512_DOUBLE_ENTRY_DB_ERROR){
            throw new Error("Server-side database error occurred. There are two double entries spotted.\n" + response.status + ": " + response.statusText);
        }
        else {
            setTimeout(function(){drawNoDeviceMessage(html_elt_id_name);},2000);
            throw new Error("An unexpected error occurred. \n" + response.status + ": " + response.statusText);
        }
    })
    .then(data => {
        data.scanned_devices.forEach(drawScannedDevices);
    })
    .catch(err => console.error(err));


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

function closeMenu(){
  var i, x; 
  /* var tablinks; */
  x = document.getElementsByClassName("selection");     // Maybe change to element ID to target just Scan??
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



function thumbnailSelect(element){
  
  $('.scanDev a.active').removeClass('active') /* select one thumbnail at a time */ 
  element.classList.toggle("active");
}




//$(window).bind("load", getPreviouslyPairedDevices());

