import requests
import geoip2.database
import os
from typing import Dict, Optional, Tuple

# Path to the GeoLite2 database file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GEOIP_DB_PATH = os.path.join(BASE_DIR, 'data', 'GeoLite2-City.mmdb')

# AbuseIPDB API settings
ABUSEIPDB_API_KEY = ""  # Add your API key here
ABUSEIPDB_API_URL = "https://api.abuseipdb.com/api/v2/check"

class IPInfo:
    def __init__(self):
        self.reader = None
        self.initialize_geoip()
    
    def initialize_geoip(self):
        """Initialize the GeoIP database reader if the database file exists."""
        try:
            if os.path.exists(GEOIP_DB_PATH):
                self.reader = geoip2.database.Reader(GEOIP_DB_PATH)
                print(f"GeoIP database loaded from {GEOIP_DB_PATH}")
                return True
            else:
                print(f"GeoIP database not found at {GEOIP_DB_PATH}")
                print("IP geolocation will use fallback data")
                # Create data directory if it doesn't exist
                os.makedirs(os.path.dirname(GEOIP_DB_PATH), exist_ok=True)
                return False
        except Exception as e:
            print(f"Error initializing GeoIP database: {e}")
            print("IP geolocation will use fallback data")
            return False
    
    def get_ip_location(self, ip: str) -> Dict:
        """Get location information for an IP address."""
        result = {
            "country": "Unknown",
            "country_code": "XX",
            "city": "Unknown",
            "latitude": 0.0,
            "longitude": 0.0
        }
        
        if not self.reader:
            return result
        
        try:
            response = self.reader.city(ip)
            result["country"] = response.country.name or "Unknown"
            result["country_code"] = response.country.iso_code or "XX"
            result["city"] = response.city.name or "Unknown"
            result["latitude"] = response.location.latitude or 0.0
            result["longitude"] = response.location.longitude or 0.0
        except Exception as e:
            print(f"Error getting location for IP {ip}: {e}")
        
        return result
    
    def check_ip_abuse(self, ip: str) -> Tuple[bool, int, str]:
        """Check if an IP is flagged as abusive using AbuseIPDB.
        
        Returns:
            Tuple containing (is_abused, confidence_score, report_message)
        """
        if not ABUSEIPDB_API_KEY:
            return False, 0, "API key not configured"
        
        try:
            headers = {
                'Accept': 'application/json',
                'Key': ABUSEIPDB_API_KEY
            }
            params = {
                'ipAddress': ip,
                'maxAgeInDays': 90,
                'verbose': False
            }
            
            response = requests.get(ABUSEIPDB_API_URL, headers=headers, params=params)
            if response.status_code == 200:
                data = response.json().get('data', {})
                score = data.get('abuseConfidenceScore', 0)
                is_abused = score > 25  # Consider IPs with score > 25% as potentially abusive
                message = f"Abuse score: {score}%"
                return is_abused, score, message
            else:
                return False, 0, f"API error: {response.status_code}"
        except Exception as e:
            return False, 0, f"Error checking abuse status: {e}"

# Singleton instance
ip_info = IPInfo()

def get_ip_info(ip: str) -> Dict:
    """Get comprehensive information about an IP address."""
    location = ip_info.get_ip_location(ip)
    
    # Only check abuse if API key is configured
    if ABUSEIPDB_API_KEY:
        is_abused, abuse_score, abuse_message = ip_info.check_ip_abuse(ip)
    else:
        # Use a simple heuristic for demo purposes - mark some IPs as abused based on last octet
        # In a real application, you would use the actual API
        last_octet = int(ip.split('.')[-1]) if '.' in ip else 0
        is_abused = last_octet > 200  # Just a demo heuristic
        abuse_score = last_octet / 2.55 if is_abused else 0  # Scale to 0-100
        abuse_message = "Demo mode - no API key configured"
    
    return {
        **location,
        "is_abused": is_abused,
        "abuse_score": abuse_score,
        "abuse_message": abuse_message
    }