/**
 * @file   This file is specific to the PID IOT project. It handles the Functional Testing section of the page.
 * @author Adonay Berhe, Felicia James
 * @since  01.11.2021
 */

function runFunctionTests() {
    var function_test_names = {"function_tests": []}
    var tests_row_elt = functional_test_elts = document.getElementById("function_tests_row");
    var tests = tests_row_elt.getElementsByTagName("li");

    for (test of tests)
    {
        function_test_names["function_tests"].push(test.id);
    }

    var url = "/send_function_tests";
    d3.json(url, {method: "POST", body: JSON.stringify(function_test_names),
    headers: {"Content-type": "application/json; charset=UTF-8"}}).then((returnVal)=>{
        /*for (indx = 0; indx < returnVal.function_tests.length; indx++)
        {
            update_function_test_elements(returnVal.function_tests[indx].test_name,
            returnVal.function_tests[indx].test_value)
        }*/
        for (test of returnVal.function_tests)
        {
            update_function_test_elements(test.test_name, test.test_value);
        }
    });
}

function update_function_test_elements(test_name, test_val)
{
    test_element = document.getElementById(test_name);
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

            if(test_val === true)
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