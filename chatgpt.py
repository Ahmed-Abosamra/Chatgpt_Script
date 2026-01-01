#!/usr/bin/env python3
import json
import random
import string
import time
import sys
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

# UI Settings
class Colors:
    RESET = "\033[0m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    CYAN = "\033[96m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[91m"  # Added RED color for error messages

# Send request to create temporary email
def make_request(url: str, payload: dict) -> tuple[int, str]:
    data = json.dumps(payload).encode("utf-8")
    request = Request(url, data=data, method="POST")
    try:
        with urlopen(request, timeout=15) as response:
            return response.status, response.read().decode("utf-8")
    except (HTTPError, URLError) as e:
        return e.code, str(e)

# Create temporary email address
def create_address() -> dict | None:
    API_URL = "https://temp-mail.lu-la.workers.dev/api/new_address"
    name = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
    payload = {"name": name, "domain": "erzi.me"}
    
    status_code, body = make_request(API_URL, payload)
    
    if status_code != 200:
        print(f"{Colors.RED}❌ Failed to create email. Status code: {status_code}{Colors.RESET}")
        return None

    try:
        data = json.loads(body)
        jwt = data.get("jwt")
        if jwt:
            email = f"{name}@erzi.me"
            link = f"https://em.bjedu.tech/en?jwt={jwt}"
            return {"email": email, "link": link}
        else:
            print(f"{Colors.RED}❌ JWT missing in the response. Unable to create email.{Colors.RESET}")
    except json.JSONDecodeError:
        print(f"{Colors.RED}❌ Failed to parse the response as JSON.{Colors.RESET}")
    return None

# Generate a random password
def generate_password(length: int = 16) -> str:
    chars = string.ascii_letters + string.digits + "!@#$%&*"
    return ''.join(random.choice(chars) for _ in range(length))

# Print credentials
def print_credentials(email: str, password: str, inbox_link: str):
    print(f"{Colors.GREEN}{Colors.BOLD}╔══════════════════════════════════════════════════════════════╗")
    print(f"║                    ✅  SUCCESS  ✅                           ║")
    print(f"╚══════════════════════════════════════════════════════════════╝{Colors.RESET}")
    print()
    print(f"  {Colors.BOLD}Your Credentials:{Colors.RESET}")
    print()
    print(f"  {Colors.BOLD}📧 Email:{Colors.RESET}    {Colors.CYAN}{email}{Colors.RESET}")
    print(f"  {Colors.BOLD}🔑 Password:{Colors.RESET} {Colors.YELLOW}{password}{Colors.RESET}")
    print()
    print(f"  {Colors.BOLD}📬 Inbox:{Colors.RESET}    {Colors.CYAN}{inbox_link}{Colors.RESET}")
    print()
    print(f"  {Colors.BOLD}{Colors.YELLOW}⚠ Save these credentials! Account expires in 24 hours.{Colors.RESET}")
    print()
    
    # Next Steps
    print(f"  {Colors.BOLD}Next Steps:{Colors.RESET}")
    print(f"  {Colors.DIM}1.{Colors.RESET} Open the inbox link above in a {Colors.BOLD}private/incognito{Colors.RESET} window")
    print(f"  {Colors.DIM}2.{Colors.RESET} Go to {Colors.CYAN}https://chatgpt.com/k12-verification{Colors.RESET}")
    print(f"  {Colors.DIM}3.{Colors.RESET} Sign up using the email and password above")
    print(f"  {Colors.DIM}4.{Colors.RESET} Check the inbox for the verification email")
    print()

# Main function
def main():
    # Generate password
    password = generate_password(16)
    
    # Create temporary email
    result = create_address()
    if result:
        email = result["email"]
        inbox_link = result["link"]
        print_credentials(email, password, inbox_link)
    else:
        print(f"{Colors.RED}❌ Email Creation Failed{Colors.RESET}")
        return 1
    return 0

if __name__ == "__main__":
    sys.exit(main())
