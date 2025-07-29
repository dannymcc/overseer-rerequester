# Overseer Re-request Script

This Python script helps you re-request all items from an Overseer instance. This is particularly useful when migrating your media server setup to a new machine while keeping Overseer on the old server.

## Features

- 🔍 **Query all requests** from your Overseer instance
- 📊 **Analyze requests** by status, media type, user, and date
- 🔄 **Re-request items** to trigger downloads on your new setup
- 🛡️ **Dry run mode** to test before making actual changes
- ⚙️ **Easy configuration** with variables at the top of the script
- 📅 **Date filtering** - only re-request items from before a specific date
- 👤 **User filtering** - only re-request items from specific users

## Setup

1. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure the script:**
   
   ⚠️ **Important:** The script contains placeholder values. You must update these with your actual Overseer details:
   
   Edit the top of `overseer_rerequest.py` to set your Overseer details:
   
   ```python
   # Configuration - Update these values for your setup
   OVERSEER_URL = "https://your-overseer-instance.com"
   API_TOKEN = "your-api-token-here"
   
   # Set to True to actually re-request items (USE WITH CAUTION!)
   DRY_RUN = True
   
   # Skip confirmation prompt in live mode (USE WITH CAUTION!)
   SKIP_CONFIRMATION = False
   
   # Request throttling - delay in seconds between requests
   REQUEST_DELAY = 1.0
   
   # For testing - limit number of requests (set to None for no limit)
   TEST_LIMIT = None
   
   # Optional filtering (set to None to disable)
   FILTER_BEFORE_DATE = None  # Example: "2024-01-01"
   FILTER_BY_USER = None      # Example: "username" or 123
   ```

3. **Get your API token:**
   - Log into your Overseer instance
   - Go to Settings → General → API Key
   - Copy the API key

## Filtering Options

The script supports powerful filtering to help you selectively re-request items:

### 📅 **Date Filtering**
Only re-request items requested before a specific date:

```python
FILTER_BEFORE_DATE = "2024-12-31"  # Only requests from before this date
```

**Use cases:**
- Migrate only older requests before your server change
- Exclude recent requests that might already be processing
- Re-request items from a specific time period

### 👤 **User Filtering**
Only re-request items from specific users:

```python
FILTER_BY_USER = "username"           # By display name
FILTER_BY_USER = 123                  # By user ID
FILTER_BY_USER = "user@example.com"   # By email address
```

**Use cases:**
- Only re-request items from specific family members
- Re-request items from users who had issues
- Exclude admin test requests

### 🔗 **Combined Filtering**
You can use both filters together:

```python
FILTER_BEFORE_DATE = "2024-12-01"
FILTER_BY_USER = "username"
# Only re-requests from username before Dec 1, 2024
```

## Usage

### Step 1: Test Connection (Dry Run)

First, run the script in dry run mode to make sure everything works:

```bash
# On most systems:
python overseer_rerequest.py

# On macOS, you may need to use python3:
python3 overseer_rerequest.py
```

This will:
- ✅ Test your connection to Overseer
- 📊 Show you statistics about your requests
- 🔍 Display sample requests
- 💭 Simulate re-requesting without actually doing it

### Step 2: Live Re-requesting (Optional)

⚠️ **CAUTION:** Only do this when you're ready to actually re-request items!

1. Change `DRY_RUN = False` in the script
2. Run the script again:
   ```bash
   # On most systems:
   python overseer_rerequest.py
   
   # On macOS, you may need to use python3:
   python3 overseer_rerequest.py
   ```
3. Confirm when prompted that you want to proceed

## What This Script Does

1. **Connects** to your Overseer instance using the API
2. **Fetches** all requests (movies, TV shows, etc.)
3. **Analyzes** the requests and shows you statistics
4. **Re-requests** each item, which should trigger your download clients

## Security Notes

- 🔐 **Your API token is sensitive** - don't share it publicly or commit it to version control
- 🛡️ The script defaults to dry run mode for safety
- 📝 Review the output carefully before enabling live mode
- 🔒 **For public repositories:** Create a `.env` file or use environment variables for credentials

## Advanced Features

### 🔍 **Debug Mode**
To see the detailed structure of requests (useful for troubleshooting):

```python
DEBUG_SHOW_REQUEST_STRUCTURE = True
```

This will show you the complete JSON structure of requests, which can help you understand what data is available.

### ⚡ **Performance & Reliability**
The script includes several features to ensure reliable operation:

- **Request throttling** - Configurable delay between requests to avoid API overload
- **Enhanced error handling** - Detailed error messages with specific failure reasons
- **Progress tracking** - Shows "Processing X/Y" during execution
- **Automatic retries** - Handles temporary API issues gracefully

### 🧪 **Testing Options**
For safe testing and incremental migration:

```python
TEST_LIMIT = 10           # Process only first 10 requests
SKIP_CONFIRMATION = True  # Skip "yes/no" prompts for automation
REQUEST_DELAY = 2.0       # Increase delay for slower API responses
```

### 📊 **Enhanced Analysis**
The script automatically shows:
- **User breakdown** - who made the most requests
- **Date patterns** - requests by month to understand usage trends
- **Detailed sample requests** - with user and date information
- **Success/failure rates** - Track migration effectiveness

## Troubleshooting

### Connection Issues
- Verify your `OVERSEER_URL` is correct (include `https://`)
- Check that your API token is valid
- Ensure your Overseer instance is accessible

### No Requests Found
- Check that you have requests in your Overseer instance
- Verify your API token has the correct permissions
- Try enabling debug mode to see the raw data structure

### Filtering Issues
- **Date format**: Use YYYY-MM-DD format (e.g., "2024-12-31")
- **User matching**: The script checks display name, email, and user ID
- **No matches**: Check the user analysis section to see available users

### Re-request Failures
- Some items might already be requested/available
- Check your Overseer logs for more details
- Ensure your download clients are properly configured

### Expected Failure Rates
During migration, it's normal to see some failures:
- **TMDB 404 errors**: Old items removed from The Movie Database
- **Data corruption errors**: Invalid metadata in Overseer database
- **Success rates of 40-60%** are typical for older request libraries
- Failed requests usually represent items that needed cleanup anyway

## Example Output

```
🎬 Overseer Re-request Script
==================================================
⚠️  DRY RUN MODE: No actual re-requests will be made
🌐 Overseer URL: https://your-overseer-instance.com

🔽 Active Filters:
   📅 Date: Only requests before 2024-12-01
   👤 User: Only requests by username

✅ Connected to Overseer successfully!
   Version: 1.34.0

🔍 Fetching requests...
   Page 1: Found 50 requests
   Page 2: Found 23 requests
📊 Total requests found: 73

🔽 Filtered: 73 → 45 requests
   📅 Date filter: before 2024-12-01
   👤 User filter: username

📈 Request Analysis:
   Status breakdown:
     2: 42
     4: 3

   Media type breakdown:
     movie: 35
     tv: 10

   👤 Top requesting users:
     username (ID: 1): 45 requests

   📅 Requests by month:
     2024-08: 5 requests
     2024-09: 8 requests
     2024-10: 12 requests
     2024-11: 20 requests

📋 Sample requests:
   1. [MOVIE] The Matrix - Status: 2
      Created: 2024-11-15T14:30:22.000Z
      Requested by: username (ID: 1)
      Request ID: 456
```

## License

This script is provided as-is for personal use. Use at your own risk. 