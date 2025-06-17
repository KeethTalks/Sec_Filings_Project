# Import required libraries
from sec_api import FullTextSearchApi  # For accessing SEC EDGAR data
from dotenv import load_dotenv        # For loading environment variables
import os                             # For interacting with the operating system
import json                           # For saving results (optional)

# Load environment variables from the .env file
load_dotenv()

# Get the API key from the .env file
API_KEY = os.getenv("SEC_API_KEY")

# Verify the API key exists to avoid runtime errors
if not API_KEY:
    print("Error: SEC_API_KEY is not set in the .env file.")
    exit(1)  # Exit the script if the key is missing

# Initialize the SEC-API full-text search with the API key
fullTextSearchApi = FullTextSearchApi(api_key=API_KEY)

# Define the search query parameters
query = {
    "query": "Bitcoin OR Ethereum OR Solana OR Cryptocurrency",  # Search for these keywords
    "formTypes": ["8-K", "10-Q", "10-K"],       # Limit to these filing types
    "startDate": "2025-06-16",                  # Start date for the search
    "endDate": "2025-06-17",                    # End date (adjust as needed)
    "size": 10                                  # Limit to 10 results
}

# Execute the search and handle potential errors
try:
    filings = fullTextSearchApi.get_filings(query)
    
    # Check if any filings were returned
    if filings["filings"]:
        print("Found filings:")
        for filing in filings["filings"]:
            # Extract key details, using .get() with defaults if data is missing
            ticker = filing.get("ticker", "N/A")                  # Ticker symbol, defaults to "N/A"
            form_type = filing.get("formType", "Unknown")         # Form type, defaults to "Unknown"
            company_name_long = filing.get("companyNameLong", "Unknown")  # Company name, defaults to "Unknown"
            filed_at = filing.get("filedAt", "Unknown")           # Filing date, defaults to "Unknown"
            url = filing.get("filingUrl", "N/A")                  # Filing URL, defaults to "N/A"
            
            # Display the details in the terminal
            print(f"- Ticker: {ticker}")
            print(f"  Form Type: {form_type}")
            print(f"  Company: {company_name_long}")
            print(f"  Filed At: {filed_at}")
            print(f"  URL: {url}")
            print("---")
    else:
        print("No filings found for the given query.")
except Exception as e:
    print(f"Error during API call: {e}")

# Optional: Save the raw data to a JSON file for reference
with open("filings.json", "w") as f:
    json.dump(filings, f, indent=2)