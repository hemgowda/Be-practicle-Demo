from django.shortcuts import render
from django.http import *
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
import subprocess
import xml.etree.ElementTree as ET
from subprocess import Popen, PIPE
import os
# Create your views here.


def home(request):
    return HttpResponse("Hello this is Django projectw3")

def csrf(request):
    return JsonResponse({'csrfToken': get_token(request)})

# def generate_robot_script(tests):
#     base_script = """*** Settings ***
#                         Library    SeleniumLibrary
#                     *** Test Cases ***
#                 """
#     for test in tests:
#         title = test['title']
#         steps = '\n    '.join(test['steps'])
#         test_case_script = f"{title}\n    [Documentation]    Automated test case for: {title}\n    {steps}\n"
#         base_script += test_case_script

#     return base_script

# def execute_robot_tests(script_path):
#     result = subprocess.run([r'C:\Users\hem\Downloads\Sanjay\P\Tests', script_path], capture_output=True, text=True)
#     return result.stdout, result.stderr

# def parse_robot_output(output_xml):
#     tree = ET.parse(output_xml)
#     root = tree.getroot()
#     results = {
#         'suite': root.find('.//suite').attrib['name'],
#         'status': root.find('.//status').attrib['status'],
#         'errors': root.find('.//status').text.strip()
#     }
#     return results

# def test_api(request):
#     test_results = parse_robot_output('path_to_output_directory/output.xml')
#     return JsonResponse(test_results)

def execute_robot_tests(test_steps):
    robot_test_content = ""
    for step in test_steps:
        robot_test_content += step + "\n"

    robot_test_file_path = r"C:\Users\hem\Downloads\Sanjay\P\Tests\test_tempate.robot"

    with open(robot_test_file_path, "w") as f:
        # Writing test settings
        f.write("*** Settings ***\n")
        f.write("Documentation    Dynamic Test\n")
        f.write("...               Created dynamically\n")
        f.write("\n")
        f.write("*** Test Cases ***\n")

        # Writing test steps
        for i, step in enumerate(test_steps, start=1):
            f.write(f"Test {i}\n")
            f.write(f"    {step}\n")
            f.write("    Log    Test Step Executed\n")
            f.write("\n")

    process = Popen(["robot", robot_test_file_path], stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()

    os.remove(robot_test_file_path)

    return stdout.decode(), stderr.decode()

def execute_tests(request):
    if request.method == 'POST':
        try:
            # Parse the JSON payload
            data = json.loads(request.body)

            # Ensure 'tests' key is in data
            if 'tests' not in data:
                return JsonResponse({'error': 'Missing tests data'}, status=400)

            # Extracting the tests data
            tests = data['tests']
            test_results = []

            # Executing tests and collect results
            for test in tests:
                title = test['title']
                steps = test['steps']
                stdout, stderr = execute_robot_tests(steps)
                test_results.append({'title': title, 'stdout': stdout, 'stderr': stderr})

            # Returning test results
            return JsonResponse({'results': test_results})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError:
            return JsonResponse({'error': 'Malformed data, missing required fields'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)





'''
#@require_http_methods(["POST"])  # This decorator ensures that only POST requests are handled
def execute_tests(request):
    if request.method == 'POST':
        try:
            # Parse the JSON payload
            data = json.loads(request.body)

            # Ensure 'tests' key is in data
            if 'tests' not in data:
                return JsonResponse({'error': 'Missing tests data'}, status=400)

            # Extract the tests data
            tests = data['tests']
            for test in tests:
                # Here, test will be a dictionary with keys 'title' and 'steps'
                title = test['title']
                steps = test['steps']
                # You can now do something with each test's details

            # Here, just return a success message for illustration
            return JsonResponse({'message': 'Tests received successfully', 'status': 'success'})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except KeyError:
            # Handle missing keys or wrong data structure
            return JsonResponse({'error': 'Malformed data, missing required fields'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    '''
# def process_tests(tests):
#     # Here you would handle the conversion and execution of tests
#     # For now, we'll just return the tests as-is
        
#     for test in tests:
#                 # Here, test will be a dictionary with keys 'title' and 'steps'
#                 title = test['title']
#                 steps = test['steps']
#                 # You can now do something with each test's details

#             # Here, just return a success message for illustration
#     return JsonResponse({'message': 'Tests received successfully', 'status': 'success'})
#     return tests
