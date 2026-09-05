# Project-Activity-3-Social-Coding# Network IP Information Tool

## Project Activity 3 - Social Coding

A Python command-line prototype for network technicians. The application retrieves public IP and network/location information using the ipapi.co REST API.

## Features

- Public IP information
- ISP / organization
- ASN
- Country and country code
- Region and city
- Timezone
- Latitude and longitude
- Refresh option
- IPv4/IPv6 display options
- Full information display
- API and connection error handling

## Requirements

- Python 3.x
- `requests`

Install the dependency:

```bash
pip install requests
```

Run:

```bash
python main.py
```

## API

The application uses:

`https://ipapi.co/json/`

The endpoint returns information associated with the public IP of the device making the request.

## Important IPv4/IPv6 Note

The API response identifies the IP version associated with the request. IPv4 and IPv6 availability depends on the network connection and whether the device has IPv6 connectivity. The application should not invent an IPv6 address when IPv6 is unavailable.

## Future Backlog

- Export reports to TXT/CSV
- IP history
- Automatic refresh
- IP change detection
- Reverse DNS lookup
- Ping/latency testing
- WHOIS lookup
- IPv4/IPv6 connectivity test
- GUI version

## Development Status

Initial technician-oriented IP information tool implementation.
The project uses a feature-branch workflow before changes are merged into the development branch.