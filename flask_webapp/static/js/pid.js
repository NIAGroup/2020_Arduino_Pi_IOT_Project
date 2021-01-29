/**
 * @file   This file is specific to the PID IOT project. It handles the Functional Testing section of the page.
 * @author Adonay Berhe
 * @since  01.29.2021
 */

// User defined macros
var baseUrl = "";

// HTTP response status codes
var HTTP_200_OK = 200;

function getConnectedDeviceName(){
    var connected_device_collection = document.getElementsByClassName("connection_status_border"); // There should only be 1 elt
    var connected_device_tag = connected_device_collection[0];
    return connected_device_tag.nextSibling.innerText;
}


/* Got the top from device_list.js*/

function sendPID(){
    payload_data = {};

    var kp_form = document.getElementById("kp");
    var ki_form = document.getElementById("ki");
    var kd_form = document.getElementById("kd");
    var angle_form = document.getElementById("angle");

    payload_data["device"] = getConnectedDeviceName();
    payload_data["kp"] = kp_form.elements[0].value;
    payload_data["ki"] = ki_form.elements[0].value;
    payload_data["kd"] = kd_form.elements[0].value;
    payload_data["angle"] = angle_form.elements[0].value;

    var url= baseUrl.concat("/send_pid");
    fetch(url, {
        method: "POST",
        headers: {"Content-type": "application/json; charset=UTF-8"},
        body: JSON.stringify(payload_data)
    })
    .then(response => {
        if (response.status === HTTP_200_OK){
            return  response.json();
        }
        else {
            throw new Error("An unexpected error occurred. \n" + response.status + ": " + response.statusText);
        }
    })
    .then(data => {
        changeRunButtonColor()
    })
    .catch(err => console.error(err));
}






function changeRunButtonColor(){
  var btn;
  btn = document.getElementById("submit_pid_btn");

  if(btn.classList.contains("btn-success")){
    btn.classList.remove("btn-success");
    btn.classList.add("btn-danger")
  }
  else if (btn.classList.contains("btn-danger")){
    btn.classList.remove("btn-danger");
    btn.classList.remove("btn-success");
  }
  else{
    btn.classList.add("btn-success");
  }
}