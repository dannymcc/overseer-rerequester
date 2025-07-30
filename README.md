# Overseer Re-request Script

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://buymeacoffee.com/d3hkz6gwle)

A Python script that helps you re-request all items from an Overseer instance with advanced filtering and migration capabilities. Perfect for migrating your media server setup to a new machine while keeping Overseer on the old server.

![Python](https://img.shields.io/badge/Python-3.7+-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Overseer](https://img.shields.io/badge/Overseer-Compatible-purple)

## 🚀 Features

- **🔍 Smart Request Querying**: Automatically fetches all requests from your Overseer instance with pagination support
- **📊 Advanced Analytics**: Detailed breakdowns by status, media type, users, and request patterns over time
- **🔄 Intelligent Re-requesting**: Triggers downloads on your new server setup with error handling and retries
- **🛡️ Safe Testing Mode**: Comprehensive dry-run functionality to preview changes before execution
- **📅 Flexible Date Filtering**: Support for date ranges (before/after) with smart handling of legacy requests
- **👤 User-Based Filtering**: Target specific users or exclude certain requesters from migration
- **🎬 Media Type Filtering**: Separate handling for movies vs TV series for staged migrations
- **⚡ Performance Controls**: Configurable request throttling and batch processing to avoid API overload
- **🔍 Enhanced Debugging**: Detailed progress tracking and comprehensive error reporting
- **🧪 Testing Features**: Limit processing to small batches for safe testing and validation
- **⚙️ Zero-Config Setup**: Simple credential configuration with automatic validation
- **📈 Migration Analytics**: Success/failure tracking with detailed reporting for large migrations

## 📦 Installation

### Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/dannymcc/overseer-rerequester.git
   cd overseer-rerequester
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the script:**
   
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
   FILTER_BEFORE_DATE = None   # Example: "2024-12-31"
   FILTER_AFTER_DATE = None    # Example: "2024-01-01"
   FILTER_MEDIA_TYPE = None    # Example: "movie" or "tv"
   FILTER_BY_USER = None       # Example: "username" or 123
   INCLUDE_INVALID_DATES = True # Include requests with missing dates
   ```

4. **Get your API token:**
   - Log into your Overseer instance
   - Go to Settings → General → API Key
   - Copy the API key

## 🔧 Requirements

- Python 3.7 or higher
- Active Overseer instance
- Valid API token with request permissions
- Network access to your Overseer server

## Filtering Options

The script supports powerful filtering to help you selectively re-request items:

### 📅 **Date Filtering**
Filter requests by date range:

```python
FILTER_BEFORE_DATE = "2024-12-31"  # Only requests before this date
FILTER_AFTER_DATE = "2024-01-01"   # Only requests after this date
# Combine both for a date range (Jan 1 - Dec 31, 2024)
```

**Use cases:**
- Migrate only requests from a specific time period
- Exclude recent requests that might already be processing
- Re-request items from before your server migration
- Process requests in chronological batches

**Date Handling:**
- Requests with missing/invalid dates are included by default
- Set `INCLUDE_INVALID_DATES = False` to exclude them

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

### 🎬 **Media Type Filtering**
Only re-request specific types of content:

```python
FILTER_MEDIA_TYPE = "movie"  # Only movies
FILTER_MEDIA_TYPE = "tv"     # Only TV shows
FILTER_MEDIA_TYPE = None     # Both movies and TV (default)
```

**Use cases:**
- Migrate movies and TV shows separately
- Test migration with only one content type first
- Different handling for movies vs TV series

### 🔗 **Combined Filtering**
You can combine multiple filters:

```python
FILTER_AFTER_DATE = "2024-01-01"
FILTER_BEFORE_DATE = "2024-12-01"
FILTER_MEDIA_TYPE = "movie"
FILTER_BY_USER = "username"
# Only movies requested by username between Jan-Dec 2024
```

## 🎯 Usage

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

## 📋 What This Script Does

1. **Connects** to your Overseer instance using the API
2. **Fetches** all requests (movies, TV shows, etc.)
3. **Analyzes** the requests and shows you statistics
4. **Re-requests** each item, which should trigger your download clients

## 🔒 Security Notes

- 🔐 **Your API token is sensitive** - don't share it publicly or commit it to version control
- 🛡️ The script defaults to dry run mode for safety
- 📝 Review the output carefully before enabling live mode
- 🔒 **For public repositories:** Create a `.env` file or use environment variables for credentials

## ⚡ Advanced Features

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

## 🐛 Troubleshooting

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
- **Missing dates**: Old requests may have invalid dates - enable `INCLUDE_INVALID_DATES = True`
- **Media types**: Use exact values "movie" or "tv" (case-insensitive)

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

## 📄 Example Output

```
🎬 Overseer Re-request Script
==================================================
⚠️  DRY RUN MODE: No actual re-requests will be made
🌐 Overseer URL: https://your-overseer-instance.com

🔽 Active Filters:
   📅 Before: 2024-12-01
   📅 After: 2024-01-01
   🎬 Media type: movie
   👤 User: username
   ⚠️  Invalid dates: included

✅ Connected to Overseer successfully!
   Version: 1.34.0

🔍 Fetching requests...
   Page 1: Found 50 requests
   Page 2: Found 23 requests
📊 Total requests found: 73

🔽 Filtered: 73 → 25 requests
   📅 Before: 2024-12-01
   📅 After: 2024-01-01
   🎬 Media type: movie
   👤 User: username

📊 Filtering breakdown:
   🗓️  Date filtered: 30
   ⚠️  Invalid dates: 5 (included)
   🎬 Media filtered: 8
   👤 User filtered: 5
   ✅ Included: 25

📈 Request Analysis:
   Status breakdown:
     2: 22
     4: 3

   Media type breakdown:
     movie: 25
     tv: 0

   👤 Top requesting users:
     username (ID: 1): 25 requests

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

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
1. Fork this repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test thoroughly with your Overseer instance
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Guidelines
- Test your changes with both dry-run and live modes
- Update documentation for new features
- Follow existing code style and patterns
- Add appropriate error handling

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Overseer](https://overseerr.dev/) team for creating an amazing media request management tool
- The Plex, Radarr, and Sonarr communities for building the ecosystem this tool supports
- Contributors and testers who helped improve this script

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/dannymcc/overseer-rerequester/issues)
- **Documentation**: This README and inline code comments
- **Community**: [Overseer Discord](https://discord.gg/PkCWJSeCk7) for general Overseer support

---

**Made with ❤️ by [Danny McClelland](https://github.com/dannymcc)**

*Not officially affiliated with Overseer or the *arr applications.* 