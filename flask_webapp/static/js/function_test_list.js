/**
 * @file   This file is specific to the PID IOT project. It handles the Functional Testing section of the page.
 * @author Adonay Berhe
 * @since  01.11.2021
 */

//import {baseUrl, HTTP_200_OK, getConnectedDeviceName} from './device_list.js';

// User defined macros
var baseUrl = "";

// HTTP response status codes
var HTTP_200_OK = 200;

function getConnectedDeviceName(){
    var connected_device_collection = document.getElementsByClassName("connection_status_border"); // There should only be 1 elt
    var connected_device_tag = connected_device_collection[0];
    return connected_device_tag.nextSibling.innerText;
}

/*  Got the top from device_list.js   */

var FUNCTIONAL_TESTS_TO_CONTAINER_MESSAGES = {
    "BT Connection": ["Sanity_BT_Echo"],
    "Video Feed": ["NULL"],
    "Sensor Detection": ["Sanity_Read_Sensor"],
    "Servo Motors": ["Sanity_Servo_Loop"]
}

function runFunctionTests() {
    var command_suite_payload = {};

    command_suite_payload["device"] = getConnectedDeviceName();
    command_suite_payload["function_tests"] = [];

    var func_tests_row_elt = document.getElementById("function_tests_row");
    var func_tests = func_tests_row_elt.getElementsByTagName("li");
    for (test of func_tests)
    {
        var single_command = {};
        single_command["name"] = test.id;
        single_command["container_messages"] = FUNCTIONAL_TESTS_TO_CONTAINER_MESSAGES[test.id]
        command_suite_payload ["function_tests"].push(single_command)
    }

    var url= baseUrl.concat("/send_function_tests");
    fetch(url, {
        method: "POST",
        headers: {"Content-type": "application/json; charset=UTF-8"},
        body: JSON.stringify(command_suite_payload)
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
        for (tests of data.function_tests)
        {
            var func_test_val = true
            console.log("Function test category: " + tests.name);
            for (test of tests.container_messages)
            {
                console.log(test.name + ": " + test.value);
                if (test.value != "Success"){
                    func_test_val = false       // If one is test fails, the function test category fails.
                    break
                }
            }
            update_function_test_elements(tests.name, func_test_val);
        }
    })
    .catch(err => console.error(err));
}

function update_function_test_elements(func_test_name, func_test_val)
{
    test_element = document.getElementById(func_test_name);
    test_status_bars = test_element.getElementsByTagName("i");
    for (child of test_status_bars)
    {
        if (child.classList.contains("status_icon"))
        {
            // Remove previous test results
            child.classList.remove("completed");
            child.classList.remove("fa-check");
            child.classList.remove("failed");
            child.classList.remove("fa-times");

            if(func_test_val === true)
            {
                child.classList.add("completed");
                child.classList.add("fa-check");
            }
            else{
                child.classList.add("failed");
                child.classList.add("fa-times");
            }
        }
    }
}