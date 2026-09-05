import ipaddress
from datetime import datetime

import requests

IPV4_ENDPOINT = "https://api.ipify.org?format=json"
IPV6_ENDPOINT = "https://api6.ipify.org?format=json"
DETAILS_ENDPOINT = "https://ipapi.co/{ip}/json/"
TIMEOUT = 10


def request_json(url):
    response = requests.get(
        url,
        timeout=TIMEOUT,
        headers={"User-Agent": "Technician-IP-Tool/1.0"},
    )
    response.raise_for_status()
    return response.json()


def get_public_ip(version):
    endpoint = IPV4_ENDPOINT if version == 4 else IPV6_ENDPOINT

    try:
        data = request_json(endpoint)
        ip = data.get("ip")

        if not ip:
            return None, "The API returned no IP address."

        parsed_ip = ipaddress.ip_address(ip)

        if parsed_ip.version != version:
            return None, f"The returned address is not IPv{version}."

        return ip, None

    except requests.exceptions.RequestException as error:
        return None, f"Connection error: {error}"
    except (ValueError, TypeError, KeyError) as error:
        return None, f"Invalid API response: {error}"


def get_ip_details(ip):
    try:
        data = request_json(DETAILS_ENDPOINT.format(ip=ip))

        if data.get("error"):
            return None, data.get("reason", "The geolocation API returned an error.")

        return data, None

    except requests.exceptions.RequestException as error:
        return None, f"Connection error: {error}"
    except (ValueError, TypeError) as error:
        return None, f"Invalid API response: {error}"


def collect_information():
    ipv4, ipv4_error = get_public_ip(4)
    ipv6, ipv6_error = get_public_ip(6)

    ipv4_details = None
    ipv6_details = None

    if ipv4:
        ipv4_details, _ = get_ip_details(ipv4)

    if ipv6:
        ipv6_details, _ = get_ip_details(ipv6)

    primary_details = ipv4_details or ipv6_details

    return {
        "ipv4": ipv4,
        "ipv6": ipv6,
        "ipv4_error": ipv4_error,
        "ipv6_error": ipv6_error,
        "ipv4_details": ipv4_details,
        "ipv6_details": ipv6_details,
        "primary_details": primary_details,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def value(data, key, default="Unavailable"):
    if not data:
        return default

    result = data.get(key)
    return result if result not in (None, "") else default


def display_ipv4(info):
    print("\n--- IPv4 Information ---")
    print(f"Public IPv4: {info['ipv4'] or 'Unavailable'}")

    if not info["ipv4"]:
        print(f"Reason: {info['ipv4_error'] or 'No IPv4 address detected.'}")
    else:
        details = info["ipv4_details"]
        print(f"ISP: {value(details, 'org')}")
        print(f"ASN: {value(details, 'asn')}")


def display_ipv6(info):
    print("\n--- IPv6 Information ---")
    print(f"Public IPv6: {info['ipv6'] or 'Unavailable'}")

    if not info["ipv6"]:
        print(f"Reason: {info['ipv6_error'] or 'No IPv6 address detected.'}")
    else:
        details = info["ipv6_details"]
        print(f"ISP: {value(details, 'org')}")
        print(f"ASN: {value(details, 'asn')}")


def display_full(info):
    print("\n========== FULL NETWORK INFORMATION ==========")
    print(f"Last updated: {info['updated_at']}")

    print("\n[IP ADDRESSES]")
    print(f"IPv4: {info['ipv4'] or 'Unavailable'}")
    print(f"IPv6: {info['ipv6'] or 'Unavailable'}")

    details = info["primary_details"]

    print("\n[NETWORK]")
    print(f"ISP/Organization: {value(details, 'org')}")
    print(f"ASN: {value(details, 'asn')}")

    print("\n[LOCATION]")
    print(f"Country: {value(details, 'country_name')}")
    print(f"Country Code: {value(details, 'country_code')}")
    print(f"Region: {value(details, 'region')}")
    print(f"City: {value(details, 'city')}")
    print(f"Timezone: {value(details, 'timezone')}")

    print("\n[COORDINATES]")
    print(f"Latitude: {value(details, 'latitude')}")
    print(f"Longitude: {value(details, 'longitude')}")

    print("\n[STATUS]")
    print("IPv4 status:", "Available" if info["ipv4"] else "Unavailable")
    print("IPv6 status:", "Available" if info["ipv6"] else "Unavailable")


def print_menu():
    print("\n" + "=" * 48)
    print("       TECHNICIAN-ORIENTED IP TOOL")
    print("=" * 48)
    print("1. Refresh Information")
    print("2. Display IPv4 Only")
    print("3. Display IPv6 Only")
    print("4. Display Full Information")
    print("5. Exit")
    print("=" * 48)


def main():
    print("Welcome to the Technician-Oriented IP Tool.")
    print("Retrieving your public network information...")

    information = collect_information()

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            print("\nRefreshing information...")
            information = collect_information()
            print("Information refreshed successfully.")

        elif choice == "2":
            display_ipv4(information)

        elif choice == "3":
            display_ipv6(information)

        elif choice == "4":
            display_full(information)

        elif choice == "5":
            print("Exiting application. Goodbye.")
            break

        else:
            print("Invalid choice. Please select 1 to 5.")


if __name__ == "__main__":
    main()
