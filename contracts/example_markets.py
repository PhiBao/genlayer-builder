# Example Market Configurations for GenLayer Prediction Markets
# These are ready-to-use market templates that users can create with one click

EXAMPLE_MARKETS = {
    "sports": [
        {
            "title": "Super Bowl 2026 Winner",
            "description": "Which team will win Super Bowl 2026? Market resolves based on official NFL results.",
            "category": "sports",
            "resolution_source": "https://www.nfl.com/super-bowl/",
            "outcomes": ["Kansas City Chiefs", "Buffalo Bills", "Baltimore Ravens", "San Francisco 49ers", "Other AFC Team", "Other NFC Team"],
            "min_stake": "0.01"
        },
        {
            "title": "NBA 2025 Championship",
            "description": "Predict the NBA Championship winner for the 2024-25 season.",
            "category": "sports", 
            "resolution_source": "https://www.nba.com/playoffs/",
            "outcomes": ["Boston Celtics", "Golden State Warriors", "Los Angeles Lakers", "Denver Nuggets", "Other Team"],
            "min_stake": "0.005"
        },
        {
            "title": "Premier League 2025 Champion",
            "description": "Which team will win the 2024-25 Premier League title?",
            "category": "sports",
            "resolution_source": "https://www.premierleague.com/",
            "outcomes": ["Manchester City", "Arsenal", "Liverpool", "Chelsea", "Manchester United", "Other"],
            "min_stake": "0.01"
        }
    ],
    
    "politics": [
        {
            "title": "US Presidential Election 2028",
            "description": "Who will win the 2028 US Presidential Election?",
            "category": "politics",
            "resolution_source": "https://apnews.com/",
            "outcomes": ["Democratic Candidate", "Republican Candidate", "Third Party/Independent"],
            "min_stake": "0.02"
        },
        {
            "title": "Next Federal Reserve Rate Decision",
            "description": "What will the Federal Reserve do with interest rates at the next FOMC meeting?",
            "category": "politics",
            "resolution_source": "https://www.federalreserve.gov/",
            "outcomes": ["Raise Rates", "Lower Rates", "Keep Rates Unchanged"],
            "min_stake": "0.01"
        },
        {
            "title": "Brexit Trade Deal Update 2025",
            "description": "Will the UK and EU agree on new trade arrangements in 2025?",
            "category": "politics", 
            "resolution_source": "https://www.bbc.com/news/politics/",
            "outcomes": ["New Deal Signed", "Negotiations Extended", "No New Agreement"],
            "min_stake": "0.015"
        }
    ],
    
    "entertainment": [
        {
            "title": "Oscars 2026 Best Picture",
            "description": "Which film will win Best Picture at the 2026 Academy Awards?",
            "category": "entertainment",
            "resolution_source": "https://oscar.go.com/",
            "outcomes": ["Top Drama Film", "Top Action/Sci-Fi Film", "Top Comedy Film", "Documentary", "International Film", "Other"],
            "min_stake": "0.005"
        },
        {
            "title": "Netflix Series Renewal",
            "description": "Will Netflix renew Stranger Things for another season in 2025?",
            "category": "entertainment",
            "resolution_source": "https://variety.com/",
            "outcomes": ["Renewed", "Cancelled", "No Decision by End of Year"],
            "min_stake": "0.01"
        },
        {
            "title": "Top Box Office 2025",
            "description": "Which movie will be the highest-grossing film of 2025 worldwide?",
            "category": "entertainment",
            "resolution_source": "https://www.boxofficemojo.com/",
            "outcomes": ["Marvel/DC Superhero Film", "Disney Animation/Pixar", "Action/Adventure Sequel", "Original Drama", "Other"],
            "min_stake": "0.01"
        }
    ],
    
    "economics": [
        {
            "title": "Bitcoin Price End of 2025",
            "description": "What will Bitcoin's price be at the end of 2025?",
            "category": "crypto",
            "resolution_source": "https://coinmarketcap.com/",
            "outcomes": ["Above $100,000", "$70,000 - $100,000", "$40,000 - $70,000", "Below $40,000"],
            "min_stake": "0.01"
        },
        {
            "title": "US GDP Growth 2025",
            "description": "What will US GDP growth be in 2025 compared to 2024?",
            "category": "economics",
            "resolution_source": "https://www.bea.gov/",
            "outcomes": ["Above 3%", "2-3%", "1-2%", "0-1%", "Negative Growth"],
            "min_stake": "0.02"
        },
        {
            "title": "Tesla Stock Performance 2025",
            "description": "How will Tesla stock perform in 2025?",
            "category": "economics",
            "resolution_source": "https://finance.yahoo.com/",
            "outcomes": ["Up >50%", "Up 20-50%", "Up 0-20%", "Down 0-20%", "Down >20%"],
            "min_stake": "0.015"
        }
    ],
    
    "crypto": [
        {
            "title": "Ethereum 2.0 Staking Rewards",
            "description": "What will Ethereum staking rewards average in 2025?",
            "category": "crypto",
            "resolution_source": "https://ethereum.org/",
            "outcomes": ["Above 6%", "4-6%", "2-4%", "Below 2%"],
            "min_stake": "0.01"
        },
        {
            "title": "DeFi Total Value Locked 2025",
            "description": "What will be the total value locked in DeFi protocols by end of 2025?",
            "category": "crypto",
            "resolution_source": "https://defipulse.com/",
            "outcomes": ["Above $200B", "$100B-$200B", "$50B-$100B", "Below $50B"],
            "min_stake": "0.02"
        },
        {
            "title": "Next Major Crypto Exchange Listing",
            "description": "Which major exchange will list the most significant new token in 2025?",
            "category": "crypto",
            "resolution_source": "https://coinbase.com/",
            "outcomes": ["Coinbase", "Binance", "Kraken", "Other Major Exchange"],
            "min_stake": "0.01"
        }
    ],
    
    "technology": [
        {
            "title": "AI Model Performance 2025",
            "description": "Which AI model will achieve the highest benchmark scores in 2025?",
            "category": "other",
            "resolution_source": "https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard",
            "outcomes": ["OpenAI GPT Series", "Google Gemini Series", "Anthropic Claude Series", "Open Source Model", "Other"],
            "min_stake": "0.01"
        },
        {
            "title": "Apple Product Launch 2025",
            "description": "What will be Apple's most significant product announcement in 2025?",
            "category": "other",
            "resolution_source": "https://apple.com/",
            "outcomes": ["New iPhone", "AR/VR Product", "Apple Car", "New Mac/iPad", "Other"],
            "min_stake": "0.015"
        }
    ]
}

# Market Creation Helpers
def get_random_market_examples(category=None, count=3):
    """Get random market examples for inspiration"""
    if category:
        return EXAMPLE_MARKETS.get(category, [])[:count]
    
    # Get examples from all categories
    all_examples = []
    for cat_examples in EXAMPLE_MARKETS.values():
        all_examples.extend(cat_examples)
    
    import random
    return random.sample(all_examples, min(count, len(all_examples)))

def validate_market_config(market_config):
    """Validate a market configuration"""
    required_fields = ["title", "description", "category", "resolution_source", "outcomes", "min_stake"]
    
    for field in required_fields:
        if field not in market_config or not market_config[field]:
            return False, f"Missing required field: {field}"
    
    if len(market_config["outcomes"]) < 2:
        return False, "Must have at least 2 outcomes"
    
    if len(market_config["outcomes"]) > 10:
        return False, "Cannot have more than 10 outcomes"
    
    try:
        float(market_config["min_stake"])
    except (ValueError, TypeError):
        return False, "min_stake must be a valid number"
    
    return True, "Valid"

# Category-specific validation
CATEGORY_VALIDATORS = {
    "sports": {
        "valid_sources": ["espn.com", "bbc.com/sport", "nfl.com", "nba.com", "premierleague.com"],
        "max_outcomes": 8,
        "suggested_min_stake": 0.01
    },
    "politics": {
        "valid_sources": ["apnews.com", "reuters.com", "bbc.com/news", "politico.com"],
        "max_outcomes": 5,
        "suggested_min_stake": 0.02
    },
    "entertainment": {
        "valid_sources": ["variety.com", "hollywoodreporter.com", "oscar.go.com"],
        "max_outcomes": 6,
        "suggested_min_stake": 0.005
    },
    "economics": {
        "valid_sources": ["bloomberg.com", "wsj.com", "yahoo.com/finance", "bea.gov"],
        "max_outcomes": 5,
        "suggested_min_stake": 0.02
    },
    "crypto": {
        "valid_sources": ["coinmarketcap.com", "coinbase.com", "ethereum.org", "defipulse.com"],
        "max_outcomes": 6,
        "suggested_min_stake": 0.01
    }
}

def get_category_suggestions(category):
    """Get suggestions for creating markets in a specific category"""
    return CATEGORY_VALIDATORS.get(category, {
        "valid_sources": ["reputable news sources"],
        "max_outcomes": 6,
        "suggested_min_stake": 0.01
    })
