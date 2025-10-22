# Market Templates and AI Enhancement Utilities for GenLayer Prediction Markets
# This file contains predefined market templates and AI prompts for different categories

MARKET_TEMPLATES = {
    "sports": {
        "resolution_sources": [
            "https://www.espn.com/",
            "https://www.bbc.com/sport/",
            "https://sports.yahoo.com/",
        ],
        "common_outcomes": {
            "match_winner": ["Team A Wins", "Team B Wins", "Draw"],
            "tournament_winner": ["Favorite", "Dark Horse", "Underdog"],
            "performance": ["Over", "Under", "Exactly"]
        },
        "ai_prompt_template": """
        Analyze this sports prediction market:
        Title: {title}
        Description: {description}
        
        Consider:
        1. Current team/player form and statistics
        2. Historical head-to-head records
        3. Injury reports and team news
        4. Home advantage factors
        5. Weather conditions (if applicable)
        6. Recent betting market trends
        
        Provide initial probability estimates and market volatility assessment.
        """
    },
    
    "politics": {
        "resolution_sources": [
            "https://www.politico.com/",
            "https://www.bbc.com/news/politics/",
            "https://apnews.com/",
            "https://www.reuters.com/"
        ],
        "common_outcomes": {
            "election": ["Candidate A", "Candidate B", "Other"],
            "policy": ["Passes", "Fails", "Modified"],
            "approval": ["Increases", "Decreases", "Stays Same"]
        },
        "ai_prompt_template": """
        Analyze this political prediction market:
        Title: {title}
        Description: {description}
        
        Consider:
        1. Current polling data and trends
        2. Historical voting patterns
        3. Economic and social factors
        4. Media coverage and public sentiment
        5. Fundraising and campaign activity
        6. Demographic shifts
        
        Assess market volatility and provide probability estimates based on available data.
        """
    },
    
    "entertainment": {
        "resolution_sources": [
            "https://variety.com/",
            "https://www.hollywoodreporter.com/",
            "https://deadline.com/",
            "https://ew.com/"
        ],
        "common_outcomes": {
            "awards": ["Winner A", "Winner B", "Winner C", "Other"],
            "box_office": ["Over $X Million", "Under $X Million"],
            "ratings": ["Hit", "Moderate", "Flop"]
        },
        "ai_prompt_template": """
        Analyze this entertainment prediction market:
        Title: {title}
        Description: {description}
        
        Consider:
        1. Past performance of similar content
        2. Star power and audience appeal
        3. Critical reception and early reviews
        4. Marketing budget and campaign effectiveness
        5. Competition and release timing
        6. Social media buzz and trending topics
        
        Evaluate market interest and probability distributions.
        """
    },
    
    "economics": {
        "resolution_sources": [
            "https://www.bloomberg.com/",
            "https://www.reuters.com/business/",
            "https://www.wsj.com/",
            "https://finance.yahoo.com/"
        ],
        "common_outcomes": {
            "market_direction": ["Bull Market", "Bear Market", "Sideways"],
            "rate_decision": ["Rate Increase", "Rate Decrease", "No Change"],
            "earnings": ["Beat Expectations", "Meet Expectations", "Miss Expectations"]
        },
        "ai_prompt_template": """
        Analyze this economic prediction market:
        Title: {title}
        Description: {description}
        
        Consider:
        1. Current economic indicators and trends
        2. Federal Reserve policy and statements
        3. Inflation data and employment statistics
        4. Global economic conditions
        5. Corporate earnings and guidance
        6. Market sentiment and technical analysis
        
        Provide risk assessment and probability analysis based on economic fundamentals.
        """
    },
    
    "crypto": {
        "resolution_sources": [
            "https://coindesk.com/",
            "https://cointelegraph.com/",
            "https://www.coinbase.com/",
            "https://coinmarketcap.com/"
        ],
        "common_outcomes": {
            "price_movement": ["Moon (>50% up)", "Pump (10-50% up)", "Crab (±10%)", "Dump (10-50% down)", "Crash (>50% down)"],
            "adoption": ["Mainstream Adoption", "Gradual Growth", "Limited Progress"],
            "regulation": ["Favorable", "Neutral", "Restrictive"]
        },
        "ai_prompt_template": """
        Analyze this cryptocurrency prediction market:
        Title: {title}
        Description: {description}
        
        Consider:
        1. Technical analysis and price patterns
        2. On-chain metrics and whale activity
        3. Regulatory developments and news
        4. Developer activity and protocol updates
        5. Institutional adoption trends
        6. Market sentiment and social metrics
        
        Assess volatility and provide probability estimates for crypto market outcomes.
        """
    }
}

def get_market_template(category):
    """Get market template for a specific category"""
    return MARKET_TEMPLATES.get(category, MARKET_TEMPLATES["sports"])

def generate_ai_analysis_prompt(title, description, category, outcomes):
    """Generate AI prompt for market analysis based on category"""
    template = get_market_template(category)
    
    base_prompt = template["ai_prompt_template"].format(
        title=title,
        description=description
    )
    
    outcomes_text = ", ".join(outcomes)
    
    full_prompt = f"""
    {base_prompt}
    
    Possible Outcomes: {outcomes_text}
    
    Respond in JSON format with:
    {{
        "probability_analysis": {{
            "outcome_1": {{"probability": 0.XX, "reasoning": "explanation"}},
            "outcome_2": {{"probability": 0.XX, "reasoning": "explanation"}},
            ...
        }},
        "market_assessment": {{
            "volatility": "low|medium|high",
            "interest_level": 1-10,
            "key_factors": ["factor1", "factor2", "factor3"],
            "confidence_score": 0.XX
        }},
        "recommended_sources": ["url1", "url2"],
        "update_frequency": "hourly|daily|weekly"
    }}
    
    Only return valid JSON, no additional text.
    """
    
    return full_prompt

def get_resolution_prompt(category, title, description, outcomes, web_data):
    """Generate resolution prompt based on category"""
    template = get_market_template(category)
    
    return f"""
    Resolve this {category} prediction market using the provided data:
    
    Market: {title}
    Description: {description}
    Possible Outcomes: {", ".join([outcome['description'] for outcome in outcomes])}
    
    Web Data Sources:
    {web_data}
    
    Category-Specific Analysis for {category.upper()}:
    {template.get('resolution_guidance', 'Standard analysis applies')}
    
    Determine which outcome occurred based on factual evidence.
    
    Respond in JSON format:
    {{
        "resolved_outcome_id": "outcome_X or null if unresolved",
        "confidence": 0.95,
        "resolution_summary": "Brief factual explanation",
        "evidence_sources": ["source1", "source2"],
        "verification_method": "how the outcome was determined",
        "resolution_timestamp": "when the event was resolved"
    }}
    
    Only return valid JSON, no additional text.
    """

# Advanced Market Making Logic
def calculate_advanced_pricing(outcome_stakes, total_stakes, market_sentiment, volatility_factor):
    """
    Advanced pricing algorithm that considers multiple factors
    """
    if total_stakes == 0:
        return 0.5  # 50% base price
    
    # Basic probability from stakes
    base_probability = float(outcome_stakes) / float(total_stakes)
    
    # Apply sentiment adjustment
    sentiment_multiplier = 1 + (market_sentiment - 0.5) * 0.2  # ±10% sentiment adjustment
    adjusted_probability = base_probability * sentiment_multiplier
    
    # Apply volatility factor
    volatility_adjustment = volatility_factor * 0.1  # Higher volatility = more price movement
    
    # Ensure probability stays within bounds
    final_probability = max(0.01, min(0.99, adjusted_probability + volatility_adjustment))
    
    return final_probability

def get_market_sentiment_factors(category):
    """Get sentiment analysis factors specific to market category"""
    factors = {
        "sports": ["team_performance", "injury_reports", "fan_sentiment", "betting_trends"],
        "politics": ["polling_data", "media_coverage", "fundraising", "endorsements"],
        "entertainment": ["social_buzz", "critic_reviews", "box_office_tracking", "award_predictions"],
        "economics": ["economic_indicators", "market_trends", "analyst_sentiment", "volatility_index"],
        "crypto": ["social_sentiment", "whale_activity", "developer_activity", "regulatory_news"]
    }
    return factors.get(category, ["general_sentiment", "market_trends"])
