#!/usr/bin/python3
"""
W3C Web Page Validator for HTML and CSS files using the
W3C API:
    https://validator.w3.org/docs/api.html

Single-File Usage
-----------------
    ./validator.py index.html

Multi-File Usage
----------------
    ./validator.py index.html header.html styles/common.css

Exit
----
    success:        exit code 0
    improper usage: exit code 1
    errors found:   exit code <error count>
"""
import requests
import sys
import os


def print_stdout(output):
    """Print output in stdout

    Parameter
    ---------
        output : str
            output to be printed out to stdout
    """

    sys.stdout.buffer.write(output.encode("utf-8"))


def print_stderr(error):
    """
    Print error in stderr

    Parameter
    ---------
        error : str
            error to be printed out to stdout
    """

    sys.stderr.buffer.write(error.encode("utf-8"))


def is_empty(file_path):
    """
    Determine if file is empty of not

    Parameter
    ---------
        file_path : str
            relative path to file being evaluated
    """

    if os.path.getsize(file_path) == 0:
        raise OSError(f"File '{file_path}' is empty.")

def validate(file_path, content_type):
    """
    Start validation of files

    Operational Note
    ----------------
        file opened in binary mode as per
        - https://requests.readthedocs.io/en/master/user/advanced/

    Parameter
    ---------
        file_path : str
            relative path to file being evaluated

        content_type : str
            content-type sent in html request header

    Return
    ------
        list
            summative results of each validated file
    """

    headers = {"Content-Type": f"{content_type}; charset=utf-8"}
    url = "https://validator.w3.org/nu/?out=json"
    data = open(file_path, "rb").read()

    response = requests.post(url, headers=headers, data=data)

    if not response.status_code < 400:
        raise ConnectionError("Unable to connect to API endpoint.")

    results = []
    messages = response.json().get("messages", [])

    for message in messages:
        if message.get("type") in ["error", "info"]:
            results.append(f"'{file_path}' => {message.get('message')}")
            continue
        results.append(
            f"[{file_path}:{message.get('lastLine')}] {message.get('message')}"
        )

    return results


def analyse(file_path):
    """
    Analysis of a file and results printout

    Parameter
    ---------
        file_path : str
            relative path to file being evaluated

    Return
    ------
        int
            a count of errors made in each file
    """

    num_errors = 0

    try:
        results = None

        if file_path.endswith(".css"):
            is_empty(file_path)
            results = validate(file_path, "text/css")
        elif file_path.endswith((".html", ".htm")):
            is_empty(file_path)
            results = validate(file_path, "text/html")
        elif file_path.endswith(".svg"):
            is_empty(file_path)
            results = validate(file_path, "image/svg+xml")
        else:
            allowed_files = "'.css', '.html', '.htm' and '.svg'"
            raise OSError(
                f"File {file_path} does not have a valid file extension.\n" +
                "Only {allowed_files} are allowed."
            )

        if len(results) > 0:
            for result in results:
                print_stderr(f"{result}\n")
                num_errors += 1
        else:
            print_stdout(f"'{file_path}' => OK\n")

    except Exception as exception:
        print_stderr(f"'{exception.__class__.__name__}' => {exception}\n")

    return num_errors


def run():
    """Runs the validation of each cli provided file"""

    num_errors = 0

    for file_path in sys.argv[1:]:
        num_errors += analyse(file_path)

    return num_errors


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_stderr("Usage: validator.py file1 file2 ...\n")
        exit(1)

    sys.exit(run())
