#!/usr/bin/env python3
"""
Overseer Re-request Script

This script connects to an Overseer instance to query all requests and optionally re-request them.
Useful when migrating to a new server setup while keeping Overseer on the old server.
"""

import requests
import json
import sys
import time
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

# Configuration - Update these values for your setup
OVERSEER_URL = "https://your-overseer-instance.com"
API_TOKEN = "your-api-token-here"

# Set to True to actually re-request items (USE WITH CAUTION!)
DRY_RUN = True

# Skip confirmation prompt in live mode (USE WITH CAUTION!)
SKIP_CONFIRMATION = False

# Request throttling - delay in seconds between requests (helps avoid API overload)
REQUEST_DELAY = 1.0

# For testing - limit number of requests (set to None for no limit)
TEST_LIMIT = None

# Filtering options (set to None to disable filtering)
# Filter by date - only re-request items requested before this date (YYYY-MM-DD format)
FILTER_BEFORE_DATE = None  # Example: "2024-01-01"

# Filter by user - only re-request items requested by specific user ID or email
FILTER_BY_USER = None  # Example: 123 or "user@example.com"

# Set to True to show detailed request structure for debugging
DEBUG_SHOW_REQUEST_STRUCTURE = False

class OverseerAPI:
    def __init__(self, url: str, token: str):
        self.base_url = url.rstrip('/')
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({
            'X-API-Key': token,
            'Content-Type': 'application/json'
        })
    
    def test_connection(self) -> bool:
        """Test if we can connect to the Overseer API"""
        try:
            response = self.session.get(f"{self.base_url}/api/v1/status")
            if response.status_code == 200:
                status_data = response.json()
                print(f"✅ Connected to Overseer successfully!")
                print(f"   Version: {status_data.get('version', 'Unknown')}")
                return True
            else:
                print(f"❌ Failed to connect: HTTP {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def get_all_requests(self) -> List[Dict[str, Any]]:
        """Retrieve all requests from Overseer"""
        all_requests = []
        page = 1
        
        print("🔍 Fetching requests...")
        
        while True:
            try:
                response = self.session.get(
                    f"{self.base_url}/api/v1/request",
                    params={'take': 50, 'skip': (page - 1) * 50}
                )
                
                if response.status_code != 200:
                    print(f"❌ Error fetching requests page {page}: HTTP {response.status_code}")
                    break
                
                data = response.json()
                requests_data = data.get('results', [])
                
                if not requests_data:
                    break
                
                all_requests.extend(requests_data)
                print(f"   Page {page}: Found {len(requests_data)} requests")
                page += 1
                
            except Exception as e:
                print(f"❌ Error fetching requests: {e}")
                break
        
        print(f"📊 Total requests found: {len(all_requests)}")
        return all_requests
    
    def show_request_structure(self, requests_list: List[Dict[str, Any]]) -> None:
        """Show detailed structure of requests for debugging"""
        if not requests_list:
            print("📭 No requests to analyze")
            return
        
        print("\n🔍 Request Structure Analysis:")
        print("=" * 60)
        
        # Show structure of first request
        sample_req = requests_list[0]
        print("📋 Sample request structure:")
        print(json.dumps(sample_req, indent=2, default=str))
        
        # Analyze available fields across all requests
        all_fields = set()
        user_fields = set()
        
        for req in requests_list:
            all_fields.update(req.keys())
            if 'requestedBy' in req and req['requestedBy']:
                user_fields.update(req['requestedBy'].keys())
        
        print(f"\n📊 Available fields in requests: {sorted(all_fields)}")
        if user_fields:
            print(f"📊 Available user fields: {sorted(user_fields)}")
        
        print("=" * 60)
    
    def filter_requests(self, requests_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Filter requests based on configured criteria"""
        filtered_requests = []
        
        for req in requests_list:
            # Check date filter
            if FILTER_BEFORE_DATE:
                try:
                    created_at_str = req.get('createdAt', '')
                    if created_at_str:
                        # Parse the ISO datetime string
                        created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
                        filter_date = datetime.fromisoformat(f"{FILTER_BEFORE_DATE}T00:00:00+00:00")
                        
                        if created_at >= filter_date:
                            continue  # Skip this request - it's after the filter date
                except (ValueError, TypeError) as e:
                    print(f"⚠️  Warning: Could not parse date for request {req.get('id', 'unknown')}: {e}")
                    continue
            
            # Check user filter
            if FILTER_BY_USER:
                requested_by = req.get('requestedBy', {})
                if requested_by:
                    user_id = requested_by.get('id')
                    user_email = requested_by.get('email', '')
                    user_name = requested_by.get('displayName', '')
                    
                    # Check if filter matches user ID, email, or display name
                    if (str(FILTER_BY_USER) != str(user_id) and 
                        str(FILTER_BY_USER).lower() != user_email.lower() and
                        str(FILTER_BY_USER).lower() != user_name.lower()):
                        continue  # Skip this request - doesn't match user filter
                else:
                    continue  # Skip requests without user info when filtering by user
            
            filtered_requests.append(req)
        
        if FILTER_BEFORE_DATE or FILTER_BY_USER:
            print(f"\n🔽 Filtered: {len(requests_list)} → {len(filtered_requests)} requests")
            if FILTER_BEFORE_DATE:
                print(f"   📅 Date filter: before {FILTER_BEFORE_DATE}")
            if FILTER_BY_USER:
                print(f"   👤 User filter: {FILTER_BY_USER}")
        
        return filtered_requests
    
    def analyze_requests(self, requests_list: List[Dict[str, Any]]) -> None:
        """Analyze and display request statistics"""
        if not requests_list:
            print("📭 No requests found")
            return
        
        # Count by status
        status_counts = {}
        media_type_counts = {}
        user_counts = {}
        date_counts = {}
        
        for req in requests_list:
            status = req.get('status', 'unknown')
            media_type = req.get('type', 'unknown')
            
            status_counts[status] = status_counts.get(status, 0) + 1
            media_type_counts[media_type] = media_type_counts.get(media_type, 0) + 1
            
            # Analyze users
            requested_by = req.get('requestedBy', {})
            if requested_by:
                user_display = requested_by.get('displayName', 'Unknown User')
                user_id = requested_by.get('id', 'unknown')
                user_key = f"{user_display} (ID: {user_id})"
                user_counts[user_key] = user_counts.get(user_key, 0) + 1
            
            # Analyze dates (by month)
            created_at_str = req.get('createdAt', '')
            if created_at_str:
                try:
                    created_at = datetime.fromisoformat(created_at_str.replace('Z', '+00:00'))
                    month_key = created_at.strftime('%Y-%m')
                    date_counts[month_key] = date_counts.get(month_key, 0) + 1
                except (ValueError, TypeError):
                    pass
        
        print("\n📈 Request Analysis:")
        print("   Status breakdown:")
        for status, count in status_counts.items():
            print(f"     {status}: {count}")
        
        print("\n   Media type breakdown:")
        for media_type, count in media_type_counts.items():
            print(f"     {media_type}: {count}")
        
        print("\n   👤 Top requesting users:")
        sorted_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)
        for user, count in sorted_users[:10]:  # Show top 10 users
            print(f"     {user}: {count} requests")
        
        print("\n   📅 Requests by month:")
        sorted_dates = sorted(date_counts.items())
        for month, count in sorted_dates[-12:]:  # Show last 12 months
            print(f"     {month}: {count} requests")
        
        # Show sample requests with more details
        print("\n📋 Sample requests:")
        for i, req in enumerate(requests_list[:5]):
            media_info = req.get('media', {})
            title = media_info.get('title', 'Unknown Title')
            status = req.get('status', 'unknown')
            req_type = req.get('type', 'unknown')
            created_at = req.get('createdAt', 'unknown')
            
            # User info
            requested_by = req.get('requestedBy', {})
            user_name = "Unknown User"
            if requested_by:
                user_name = requested_by.get('displayName', 'Unknown User')
                user_id = requested_by.get('id', 'unknown')
                user_name = f"{user_name} (ID: {user_id})"
            
            print(f"   {i+1}. [{req_type.upper()}] {title} - Status: {status}")
            print(f"      Created: {created_at}")
            print(f"      Requested by: {user_name}")
            print(f"      Request ID: {req.get('id', 'unknown')}")
            print()
    
    def create_request(self, media_id: int, media_type: str, title: str = "Unknown Title") -> bool:
        """Create a new request for the specified media"""
        if DRY_RUN:
            print(f"   [DRY RUN] Would re-request {media_type} with media ID: {media_id}")
            return True
        
        try:
            payload = {
                'mediaId': media_id,
                'mediaType': media_type
            }
            
            response = self.session.post(
                f"{self.base_url}/api/v1/request",
                json=payload
            )
            
            if response.status_code in [200, 201]:
                print(f"   ✅ Successfully re-requested {media_type} (ID: {media_id})")
                return True
            else:
                # Try to get more detailed error info
                error_detail = "Unknown error"
                try:
                    error_data = response.json()
                    error_detail = error_data.get('message', error_data.get('error', str(error_data)))
                except:
                    error_detail = response.text[:100] if response.text else "No error details"
                
                print(f"   ❌ Failed to re-request {media_type} '{title}' (ID: {media_id})")
                print(f"      HTTP {response.status_code}: {error_detail}")
                return False
                
        except Exception as e:
            print(f"   ❌ Error re-requesting {media_type} '{title}' (ID: {media_id}): {e}")
            return False

def main():
    print("🎬 Overseer Re-request Script")
    print("=" * 50)
    
    # Check for placeholder values
    if OVERSEER_URL == "https://your-overseer-instance.com" or API_TOKEN == "your-api-token-here":
        print("❌ Configuration Error!")
        print("   You must update the OVERSEER_URL and API_TOKEN values at the top of this script.")
        print("   These are currently set to placeholder values.")
        print("\n   Edit the script and set:")
        print(f"   - OVERSEER_URL = \"https://your-actual-overseer-url.com\"")
        print(f"   - API_TOKEN = \"your-actual-api-token\"")
        print("\n   Get your API token from: Overseer Settings → General → API Key")
        sys.exit(1)
    
    if DRY_RUN:
        print("⚠️  DRY RUN MODE: No actual re-requests will be made")
    else:
        print("🚨 LIVE MODE: Requests WILL be created!")
    
    print(f"🌐 Overseer URL: {OVERSEER_URL}")
    
    # Show active filters
    if FILTER_BEFORE_DATE or FILTER_BY_USER:
        print("\n🔽 Active Filters:")
        if FILTER_BEFORE_DATE:
            print(f"   📅 Date: Only requests before {FILTER_BEFORE_DATE}")
        if FILTER_BY_USER:
            print(f"   👤 User: Only requests by {FILTER_BY_USER}")
    
    print()
    
    # Initialize API client
    api = OverseerAPI(OVERSEER_URL, API_TOKEN)
    
    # Test connection
    if not api.test_connection():
        print("Exiting due to connection failure.")
        sys.exit(1)
    
    print()
    
    # Get all requests
    all_requests = api.get_all_requests()
    
    if not all_requests:
        print("No requests found. Exiting.")
        sys.exit(0)
    
    # Show request structure if debug is enabled
    if DEBUG_SHOW_REQUEST_STRUCTURE:
        api.show_request_structure(all_requests)
    
    # Apply filters
    filtered_requests = api.filter_requests(all_requests)
    
    if not filtered_requests:
        print("No requests match the specified filters. Exiting.")
        sys.exit(0)
    
    # Analyze requests
    api.analyze_requests(filtered_requests)
    
    # Ask user if they want to proceed with re-requesting
    print("\n" + "=" * 50)
    
    if DRY_RUN:
        print("This is a dry run. No actual requests will be made.")
        print("Set DRY_RUN = False in the script to enable actual re-requesting.")
    else:
        if SKIP_CONFIRMATION:
            print(f"⚠️ SKIP_CONFIRMATION=True: Proceeding to re-request {len(filtered_requests)} items...")
        else:
            response = input(f"Do you want to re-request all {len(filtered_requests)} items? (yes/no): ")
            if response.lower() != 'yes':
                print("Aborted by user.")
                sys.exit(0)
    
    # Apply test limit if set
    requests_to_process = filtered_requests
    if TEST_LIMIT is not None:
        requests_to_process = filtered_requests[:TEST_LIMIT]
        print(f"\n🧪 TEST MODE: Processing only first {len(requests_to_process)} requests")
    
    # Process re-requests
    print(f"\n🔄 Processing re-requests for {len(requests_to_process)} items...")
    if not DRY_RUN:
        print(f"⏳ Adding {REQUEST_DELAY}-second delay between requests to avoid API overload...")
    
    success_count = 0
    failed_count = 0
    
    for i, req in enumerate(requests_to_process, 1):
        media_info = req.get('media', {})
        media_id = media_info.get('id')
        media_type = req.get('type', 'movie')  # Default to movie
        title = media_info.get('title', 'Unknown Title')
        
        if media_id:
            print(f"Processing {i}/{len(requests_to_process)}: {title}")
            if api.create_request(media_id, media_type, title):
                success_count += 1
            else:
                failed_count += 1
                
            # Add delay between requests to avoid overwhelming the API (except in dry run)
            if not DRY_RUN and i < len(requests_to_process):
                time.sleep(REQUEST_DELAY)
        else:
            print(f"⚠️  Skipping {title}: No media ID found")
            failed_count += 1
    
    print(f"\n📊 Re-request Summary:")
    print(f"   ✅ Successful: {success_count}")
    print(f"   ❌ Failed: {failed_count}")
    print(f"   📝 Total processed: {len(requests_to_process)}")
    if TEST_LIMIT is not None:
        print(f"   🧪 Test mode: Only processed first {TEST_LIMIT} of {len(filtered_requests)} total requests")

if __name__ == "__main__":
    main() 