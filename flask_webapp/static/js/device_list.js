/**
 * @file   This file is specific to the PID IOT project. It defines the functionality of device menus.
 * @author Adonay Berhe, Felicia James
 * @since  10.14.2020
 */

// User defined macros
var baseUrl = "";

// HTTP response status codes
var HTTP_200_OK = 200;
var HTTP_201_CREATED = 201;
var HTTP_202_ACCEPTED = 202;
var HTTP_204_NO_CONTENT = 204;
var HTTP_404_NOT_FOUND = 404;
var HTTP_512_DOUBLE_ENTRY_DB_ERROR = 512;
var HTTP_514_WRONG_DEVICE_CONNECTED_DB_ERROR = 514;
var HTTP_515_NO_DEVICE_RETURNED = 515;

// ....................... Function definitions ..................... //

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
  dev_a_tag.classList.add(rowName);
  if (device.status === "connected"){
    dev_a_tag = changeDeviceATagToConnectedStatus(dev_a_tag);
  }
  dev_a_tag.setAttribute("onclick", "thumbnailSelect(this)");
  dev_a_tag.appendChild(dev_image);

  var dev_paragraph = document.createElement("p");
  dev_paragraph.setAttribute("style", "text-align:center");
  var dev_name_text = document.createTextNode(device.name);
  dev_paragraph.appendChild(dev_name_text);

  var dev_column = document.createElement("div");
  dev_column.classList = "col Devs";
  dev_column.id = device.name;
  dev_column.appendChild(dev_a_tag);
  dev_column.appendChild(dev_paragraph);

  var dev_row = document.getElementById(rowName);
  dev_row.appendChild(dev_column);
}

function drawScannedDevices(name, index){
  drawDevicesInRows(name, index, "Scan");
}

function drawPreviouslyPairedDevices(device, index){
  drawDevicesInRows(device, index, "PreviousPaired");
}

function getSelectedDevices(){
  var devices = document.getElementsByClassName("Devs");
  var selectedDevices = {};
  for (device of devices)
  {
    devChilda = device.getElementsByTagName('a')[0];
    devChildp = device.getElementsByTagName('p')[0];
    if (devChilda.classList.contains('active'))
    {
      selectedDevices[devChildp.innerText] = [devChilda, devChildp];
    }
  }

  return selectedDevices;
}

function getDeviceByName(devName){
    var devices = document.getElementsByClassName("Devs");
    var retOptions = [];
    for (device of devices){
        devChilda = device.getElementsByTagName('a')[0];
        devChildp = device.getElementsByTagName('p')[0];
        if (devChildp.innerText === devName){
            var device_dict = {};
            device_dict[devName] = [devChilda, devChildp];
            retOptions.push(device_dict);
        }
    }
    retVal = {};
    // If device appears in both scan and previously paired
    if (retOptions.length == 2){
        for (option of retOptions){
            Object.entries(option).forEach(([devName, dev_elts]) => {
                if (dev_elts[0].classList.contains("Scan")){    // grab the a_tag [a_tag, p] and check for Scan class
                    retVal = option;            // Priority to the device in Scan row
                }
            });
        }
    }
    else{   // else device is newly scanned
        retVal = retOptions;
    }
    return retVal;
}

function getConnectedDeviceName(){
    var connected_device_collection = document.getElementsByClassName("connection_status_border"); // There should only be 1 elt
    var connected_device_tag = connected_device_collection[0];
    return connected_device_tag.nextSibling.innerText;
}

function getConnectedDeviceATag(){
    return document.getElementsByClassName("connection_status_border")[0]; // There should only be 1 elt
}

function thumbnailSelect(element){
    $('.Devs a.active').removeClass('active') /* select one thumbnail at a time */
    element.classList.toggle("active");
    // Connect button changes to Connect or Disconnect depending on current device status
    if(element.classList.contains("connection_status_border")){
        changeConnectBtnToDisconnect();
    }
    else{
        changeDisconnectBtnToConnect();
    }
}

function changeDeviceATagToConnectedStatus(devATag){
    devATag.classList.add("connection_status_border");
    devATag.setAttribute("style", "border-color : green", "border-width : thick");
    return devATag;
}

function changeDeviceATagToDisconnectedStatus(devATag){
    if (devATag.classList.contains("connection_status_border")) {
        devATag.classList.remove("connection_status_border");
        devATag.style.removeProperty("border-color");
        devATag.style.removeProperty("border-width");
    }

    return devATag;
}

function changeConnectBtnToDisconnect(){
    var connect_btn = document.getElementById("connectBtn");
    if (!connect_btn.classList.contains("btn-danger")){
        connect_btn.classList.add("btn-danger");
        connect_btn.innerHTML = "Disconnect";
    }
}

function changeDisconnectBtnToConnect(){
    var connect_btn = document.getElementById("connectBtn");
    if (connect_btn.classList.contains("btn-danger")){
        connect_btn.classList.remove("btn-danger");
        connect_btn.innerHTML = "Connect";
    }
}

function sendConnect(){
    var deviceNames = {};
    var selectedDevices = getSelectedDevices();
    if($.isEmptyObject(selectedDevices))
    {
    return;
    }
    deviceNames["selectedDevices"]  = Object.keys(selectedDevices);
    var url= baseUrl.concat("/connect");
    fetch(url, {
        method: "POST",
        headers: {"Content-type": "application/json; charset=UTF-8"},
        body: JSON.stringify(deviceNames)
    })
    .then(response => {
        if ((response.status === HTTP_201_CREATED) || (response.status === HTTP_202_ACCEPTED)){
            return  response.json();
        }
        else if (response.status === HTTP_512_DOUBLE_ENTRY_DB_ERROR){
            throw new Error("Database has double entries for device " + deviceNames["selectedDevices"][0]);
        }
        else {
            throw new Error("An unexpected error occurred. \n" + response.status + ": " + response.statusText);
        }
    })
    .then(data => {
        if ("disconnected_device" in data){     // if there was a prior connection
            var last_connected_dev_name = getConnectedDeviceName();
            if (last_connected_dev_name === data.disconnected_device.name){
                var last_connected_dev_a_tag = getConnectedDeviceATag();
                changeDeviceATagToDisconnectedStatus(last_connected_dev_a_tag);
            }
            else{
                throw Error("Client and server miss-match. Connected device client: " + last_connected_dev_name + " != server: " + data.disconnected_device.name);
            }
        }
        if ("connected_device" in data){        // connect device here
            var device_to_be_connected = getDeviceByName(data.connected_device.name); // returns {"dev_name": [a_tag, p]}
            var device_to_be_connected_a_tag = device_to_be_connected[data.connected_device.name][0];
            changeDeviceATagToConnectedStatus(device_to_be_connected_a_tag);
            changeConnectBtnToDisconnect();
        }
        else{
            throw Error("Connection did not occur or server didn't send any entries...\nExpecting entry: " + deviceNames["selectedDevices"][0]);    // Should only be 1 entry in the list
        }
    })
    .catch(err => console.error(err));
}

function sendDisconnect(){
    var deviceNames = {};
    var selectedDevices = getSelectedDevices();
    if($.isEmptyObject(selectedDevices))
    {
    return;
    }
    deviceNames["selectedDevices"]  = Object.keys(selectedDevices);
    var url= baseUrl.concat("/disconnect");
    fetch(url, {
        method: "PUT",
        headers: {"Content-type": "application/json; charset=UTF-8"},
        body: JSON.stringify(deviceNames)
    })
    .then(response => {
        if (response.status === HTTP_202_ACCEPTED){
            return  response.json();
        }
        else if (response.status === HTTP_512_DOUBLE_ENTRY_DB_ERROR){
            throw new Error("Database has double entries for device " + deviceNames["selectedDevices"][0]);
        }
        else if (response.status === HTTP_514_WRONG_DEVICE_CONNECTED_DB_ERROR){
            throw new Error("Database has a different device than " + deviceNames["selectedDevices"][0] + " logged as connected. Check server logs for more info.")
        }
        else if (response.status == HTTP_515_NO_DEVICE_RETURNED){
            throw new Error("Database has no device logged under device name: " + deviceNames["selectedDevices"][0])
        }
        else {
            throw new Error("An unexpected error occurred. \n" + response.status + ": " + response.statusText);
        }
    })
    .then(data => {
        if ("disconnected_device" in data){     // if there was a prior connection
            var connected_dev_name = getConnectedDeviceName();
            if (connected_dev_name === data.disconnected_device.name){
                var last_connected_dev_a_tag = getConnectedDeviceATag();
                changeDeviceATagToDisconnectedStatus(last_connected_dev_a_tag);
                changeDisconnectBtnToConnect();
            }
            else{
                throw Error("Client and server miss-match. Connected device client: " + connected_dev_name + " != server: " + data.disconnected_device.name);
            }
        }
        else{
            throw Error("Disconnection did not occur or server didn't send any entries...\nExpecting entry: " + deviceNames["selectedDevices"][0]);    // Should only be 1 entry in the list
        }
    })
    .catch(err => console.error(err));
}

function triggerConnection(connectBtn){
    if (connectBtn.innerText === "Connect"){
        sendConnect()
    }
    else{
        sendDisconnect()
    }
}


