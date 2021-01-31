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
    var payload_data = {};
    payload_data["device"] = getConnectedDeviceName();
    payload_data["command"] = "PID_Controller";

    // Get param values from Input Table forms
    var kp = document.getElementById("kp").elements[0].value;
    var ki = document.getElementById("ki").elements[0].value;
    var kd = document.getElementById("kd").elements[0].value;
    var angle = document.getElementById("angle").elements[0].value;

    var params = {};
    params["kp"] = kp;
    params["ki"] = ki;
    params["kd"] = kd;
    params["angle"] = angle;

    payload_data["args"] = params;

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
        var btn = document.getElementById("submit_pid_btn");
        if (data.value === "Success"){
            populateTable(kp, ki, kd, angle, data.btime);
            changePIDRunButtonToSuccess(btn);
        }
        else{
            changePIDRunButtonToFailure(btn);
        }
        setTimeout(changePIDRunButtonToNeutral, 2000, btn);
    })
    .catch(err => console.error(err));
}

function changePIDRunButtonToSuccess(btn){
    btn.classList.add("btn-success");
}

function changePIDRunButtonToFailure(btn){
    btn.classList.add("btn-danger");
}

function changePIDRunButtonToNeutral(btn){
    if(btn.classList.contains("btn-success")){
        btn.classList.remove("btn-success");
    }
    if(btn.classList.contains("btn-danger")){
        btn.classList.remove("btn-danger");
    }
}

function populateTable(kp, ki, kd, angle, btime){
// Probably need to get timestamp here.
}

/*
function streamVideo(){
    var vf_row = document.getElementById("videofeed_col");
    clearChildNodes("videofeed_col");

    var vf_img = document.createElement("img");
    vf_img.setAttribute("style", "width:100%;height:100%");
    var src_data;

    var url= "/get_video_feed";
        fetch(url, {
            method: "GET",
            headers: {"Content-type": "multipart/x-mixed-replace; boundary=frame"},
        })
        .then(response => {
            if (response.status === HTTP_200_OK){
                return  response.json();
            }
            else if (response.status === HTTP_404_NOT_FOUND){
                src_data = null;
            }
            else {
                throw new Error("An unexpected error occurred. \n" + response.status + ": " + response.statusText);
            }
        })
        .then(data => {
            src_data = data
        })
        .catch(err => console.error(err));

    //var vf_row = document.getElementById("videofeed_col");
    //clearChildNodes("videofeed_col");
    //var vf_img = document.createElement("img");
    //vf_img.setAttribute("style", "width:100%;height:100%");
    vf_img.setAttribute("src", src_data);
    vf_img.setAttribute("alt","Video Feed Not Available");
    vf_row.appendChild(vf_img);

    var vf_btn = document.getElementById("videoBtn");
    vf_btn.onclick= function(){endVideo()};
    vf_btn.setAttribute("data-toggle","popover");
    vf_btn.setAttribute("data-container","body");
    vf_btn.setAttribute("data-content","Click to turn off camera");
    <!-- vf_btn.setAttribute("onClick",'endVideo'); -->
    document.querySelector('#videoBtn').innerHTML = 'End Video';
}
*/