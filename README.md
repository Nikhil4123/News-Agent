# Indian News Fetcher

A Python script to fetch and display today's top news from Indian news channels.

## Features

- Fetches top headlines from Indian news sources using NewsAPI.org
- Displays news with title, source, publication date, and description
- Clean, formatted output for easy reading
- Multiple ways to provide API key (config file, environment variable, or user input)

## Requirements

- Python 3.x
- NewsAPI.org API key (free)

## Installation

1. Clone or download this repository
2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Setup

### Option 1: Using config.txt file (Recommended)
1. Get a free API key from [NewsAPI.org](https://newsapi.org/)
2. Open `config.txt` and add your API key:
   ```
   NEWS_API_KEY=your_actual_api_key_here
   ```

### Option 2: Using environment variables
Set the API key as an environment variable:
```bash
# On Windows (Command Prompt)
set NEWS_API_KEY=your_api_key_here

# On Windows (PowerShell)
$env:NEWS_API_KEY="your_api_key_here"

# On macOS/Linux
export NEWS_API_KEY=your_api_key_here
```

### Option 3: Interactive input
When you run the script, it will prompt you to enter your API key if it's not found in the config file or environment variables.

## Usage

Run the script:
```bash
python news_fetcher.py
```

The script will display today's top news from Indian sources.

## Example Output

```
====================================================================================================
TOP NEWS FROM INDIA - 2025-10-26
====================================================================================================

1. India's Economy Grows by 7.8% in Q2
   Source: The Hindu
   Published: 2025-10-26 10:30:00
   Description: India's economy shows strong growth in the second quarter, beating expectations...
   Link: https://example.com/article1
----------------------------------------------------------------------------------------------------

2. New Policy Announced for Digital Taxation
   Source: Times of India
   Published: 2025-10-26 09:15:00
   Description: Government introduces new framework for taxing digital services from multinational...
   Link: https://example.com/article2
----------------------------------------------------------------------------------------------------
```

## How It Works

The script uses the NewsAPI.org service to fetch current headlines from Indian news sources. It tries multiple sources to ensure the best results:
1. Google News India (primary source)
2. Country-specific headlines for India
3. General search for "India"

## Troubleshooting

- If you get an error about the API key, make sure you've registered at NewsAPI.org and obtained a valid key
- If you see "No articles found", check your internet connection and API key
- For any other issues, check the error messages displayed by the script

## Note on NewsAPI.org Free Tier Limitations

The free tier of NewsAPI.org has some limitations:
- Limited to 100 requests per day
- Limited to 1000 requests per month
- Access to news articles may be restricted after a certain time period

For production use, consider upgrading to a paid plan at NewsAPI.org.