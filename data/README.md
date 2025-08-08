# GeoIP Database

This directory is used to store the GeoLite2 City database file for IP geolocation.

## How to get the database

1. Create a free account at MaxMind: https://www.maxmind.com/en/geolite2/signup
2. Generate a license key in your account dashboard
3. Download the GeoLite2 City database in .mmdb format
4. Place the downloaded file in this directory and rename it to `GeoLite2-City.mmdb`

Alternatively, you can set the path to your database file in the `utils/ip_info.py` file.