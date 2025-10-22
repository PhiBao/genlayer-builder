# { "Depends": "py-genlayer:test" }

import json
import re
from dataclasses import dataclass
from typing import List, Dict, Optional
from genlayer import *


@allow_storage
@dataclass
class MarketOutcome:
    id: str
    description: str
    total_stakes: u256
    share_price: u256  # Current price per share (in wei)


@allow_storage
@dataclass
class Market:
    id: str
    title: str
    description: str
    category: str  # sports, politics, entertainment, economics, crypto
    creator: Address
    creation_date: str
    resolution_date: str
    resolution_source: str
    status: str  # active, resolved, cancelled
    outcomes: List[MarketOutcome]
    total_volume: u256
    resolved_outcome_id: str
    resolution_data: str
    min_stake: u256


@allow_storage
@dataclass
class UserPosition:
    market_id: str
    outcome_id: str
    shares: u256
    total_invested: u256
    average_price: u256


class PredictionMarket(gl.Contract):
    markets: TreeMap[str, Market]
    user_positions: TreeMap[Address, TreeMap[str, UserPosition]]
    user_balances: TreeMap[Address, u256]
    market_counter: u256

    def __init__(self):
        self.market_counter = 0

    def _generate_market_id(self) -> str:
        self.market_counter += 1
        return f"market_{self.market_counter}"

    def _calculate_market_sentiment(self, title: str, description: str, category: str) -> dict:
        """Enhanced AI-powered market sentiment analysis with category-specific intelligence"""
        def analyze_sentiment() -> str:
            # Category-specific analysis prompts
            category_prompts = {
                "sports": f"""
                Sports Market Analysis:
                Title: {title}
                Description: {description}
                
                Consider sports-specific factors:
                - Current team/player form and recent performance
                - Head-to-head historical records
                - Injury reports and team news
                - Home field advantage
                - Weather conditions (if applicable)
                - Betting market trends and public sentiment
                - Season context and playoff implications
                """,
                "politics": f"""
                Political Market Analysis:
                Title: {title}
                Description: {description}
                
                Consider political factors:
                - Current polling data and historical accuracy
                - Demographic trends and voter turnout patterns
                - Economic conditions and approval ratings
                - Media coverage and campaign funding
                - Historical precedents and electoral patterns
                - Social and cultural factors
                """,
                "entertainment": f"""
                Entertainment Market Analysis:
                Title: {title}
                Description: {description}
                
                Consider entertainment factors:
                - Past performance of similar content
                - Star power and audience appeal
                - Critical reception and early reviews
                - Marketing budget and promotional campaign
                - Release timing and competition
                - Social media buzz and cultural trends
                """,
                "economics": f"""
                Economic Market Analysis:
                Title: {title}
                Description: {description}
                
                Consider economic factors:
                - Current economic indicators (GDP, inflation, employment)
                - Federal Reserve policy and interest rates
                - Global economic conditions and geopolitical events
                - Corporate earnings and market sentiment
                - Technical analysis and market trends
                - Institutional investor behavior
                """,
                "crypto": f"""
                Cryptocurrency Market Analysis:
                Title: {title}
                Description: {description}
                
                Consider crypto-specific factors:
                - Technical analysis and price patterns
                - On-chain metrics and whale activity
                - Regulatory developments and institutional adoption
                - Developer activity and protocol updates
                - Market sentiment and social metrics
                - DeFi ecosystem and tokenomics
                """
            }
            
            base_prompt = category_prompts.get(category, f"""
            General Market Analysis:
            Title: {title}
            Description: {description}
            Category: {category}
            """)
            
            task = f"""
{base_prompt}

Provide comprehensive market analysis with:

1. Probability Assessment: Analyze likely outcomes based on available information
2. Market Dynamics: Consider volatility, interest level, and key risk factors
3. Sentiment Analysis: Evaluate public opinion and market sentiment
4. Confidence Score: Rate your confidence in the analysis

Respond in JSON format:
{{
    "probability_estimates": {{
        "high_probability_outcome": 0.45,
        "medium_probability_outcome": 0.35,
        "low_probability_outcome": 0.20
    }},
    "market_metrics": {{
        "volatility": "low|medium|high",
        "interest_level": 8,
        "confidence_score": 0.85,
        "complexity": "simple|moderate|complex"
    }},
    "key_factors": [
        "factor1: impact description",
        "factor2: impact description", 
        "factor3: impact description"
    ],
    "risk_assessment": {{
        "primary_risks": ["risk1", "risk2"],
        "black_swan_probability": 0.05,
        "information_quality": "high|medium|low"
    }},
    "recommended_setup": {{
        "min_stake_suggestion": "0.01",
        "resolution_timeline": "immediate|hours|days|weeks",
        "update_frequency": "realtime|hourly|daily"
    }}
}}

Only return valid JSON, no additional text.
            """
            result = gl.exec_prompt(task)
            # Clean the response
            cleaned = result.replace("```json", "").replace("```", "").strip()
            return json.dumps(json.loads(cleaned), sort_keys=True)

        result_json = json.loads(gl.eq_principle_strict_eq(analyze_sentiment))
        return result_json

    def _resolve_market_with_ai(self, market: Market) -> dict:
        """AI-powered market resolution using web data and analysis"""
        def get_resolution_data() -> str:
            # Fetch web data if resolution source is a URL
            if market.resolution_source.startswith("http"):
                web_data = gl.get_webpage(market.resolution_source, mode="text")
            else:
                web_data = market.resolution_source

            task = f"""
Resolve this prediction market based on the provided data:

Market: {market.title}
Description: {market.description}
Category: {market.category}
Possible Outcomes: {[outcome.description for outcome in market.outcomes]}

Data Source:
{web_data}

Determine which outcome occurred. Respond in JSON:
{{
    "resolved_outcome_id": "outcome_id or null if unresolved",
    "confidence": 0.95,
    "resolution_summary": "Brief explanation of what happened",
    "evidence": "Key evidence from the data supporting this resolution"
}}

Only return valid JSON, no additional text.
            """
            result = gl.exec_prompt(task)
            cleaned = result.replace("```json", "").replace("```", "").strip()
            return json.dumps(json.loads(cleaned), sort_keys=True)

        result_json = json.loads(gl.eq_principle_strict_eq(get_resolution_data))
        return result_json

    def _calculate_share_price(self, outcome: MarketOutcome, total_market_stakes: u256) -> u256:
        """Simple automated market maker - calculates share price based on current stakes"""
        if total_market_stakes == 0:
            return 500000000000000000  # 0.5 ETH initial price
        
        # Basic AMM: price increases with more stakes on this outcome
        outcome_ratio = float(outcome.total_stakes) / float(total_market_stakes)
        base_price = 100000000000000000  # 0.1 ETH
        max_price = 900000000000000000   # 0.9 ETH
        
        # Price curve: more stakes = higher price
        price = int(base_price + (outcome_ratio * (max_price - base_price)))
        return u256(price)

    @gl.public.write
    def create_market(
        self,
        title: str,
        description: str,
        category: str,
        resolution_date: str,
        resolution_source: str,
        outcomes: List[str],
        min_stake_eth: str = "0.01"
    ) -> str:
        """Create a new prediction market with AI-suggested initial setup"""
        
        # Validate inputs
        if len(outcomes) < 2 or len(outcomes) > 10:
            raise Exception("Market must have between 2 and 10 outcomes")
        
        if category not in ["sports", "politics", "entertainment", "economics", "crypto", "other"]:
            raise Exception("Invalid category")

        market_id = self._generate_market_id()
        min_stake = u256(int(float(min_stake_eth) * 1000000000000000000))  # Convert ETH to wei

        # Get AI sentiment analysis
        sentiment = self._calculate_market_sentiment(title, description, category)

        # Create market outcomes with initial equal pricing
        market_outcomes = []
        initial_price = u256(500000000000000000)  # 0.5 ETH
        
        for i, outcome_desc in enumerate(outcomes):
            outcome = MarketOutcome(
                id=f"outcome_{i+1}",
                description=outcome_desc,
                total_stakes=u256(0),
                share_price=initial_price
            )
            market_outcomes.append(outcome)

        # Create the market
        market = Market(
            id=market_id,
            title=title,
            description=description,
            category=category,
            creator=gl.message.sender_address,
            creation_date="2025-10-19",  # You could make this dynamic
            resolution_date=resolution_date,
            resolution_source=resolution_source,
            status="active",
            outcomes=market_outcomes,
            total_volume=u256(0),
            resolved_outcome_id="",
            resolution_data="",
            min_stake=min_stake
        )

        self.markets[market_id] = market
        return market_id

    @gl.public.write
    def place_bet(self, market_id: str, outcome_id: str) -> None:
        """Place a bet on a specific outcome"""
        if market_id not in self.markets:
            raise Exception("Market not found")
        
        market = self.markets[market_id]
        if market.status != "active":
            raise Exception("Market is not active")

        # Find the outcome
        outcome_index = -1
        for i, outcome in enumerate(market.outcomes):
            if outcome.id == outcome_id:
                outcome_index = i
                break
        
        if outcome_index == -1:
            raise Exception("Outcome not found")

        sender = gl.message.sender_address
        stake_amount = gl.message.value

        if stake_amount < market.min_stake:
            raise Exception(f"Minimum stake is {market.min_stake}")

        # Calculate current share price
        total_market_stakes = sum(outcome.total_stakes for outcome in market.outcomes)
        current_price = self._calculate_share_price(market.outcomes[outcome_index], total_market_stakes)
        shares_purchased = u256(int(float(stake_amount) / float(current_price) * 1000000000000000000))

        # Update outcome stakes
        market.outcomes[outcome_index].total_stakes += stake_amount
        market.total_volume += stake_amount

        # Update user position
        position_key = f"{market_id}_{outcome_id}"
        user_positions = self.user_positions.get_or_insert_default(sender)
        
        if position_key in user_positions:
            # Update existing position
            position = user_positions[position_key]
            old_total_shares = position.shares
            old_total_invested = position.total_invested
            
            position.shares += shares_purchased
            position.total_invested += stake_amount
            position.average_price = u256(int(float(position.total_invested) / float(position.shares) * 1000000000000000000))
        else:
            # Create new position
            position = UserPosition(
                market_id=market_id,
                outcome_id=outcome_id,
                shares=shares_purchased,
                total_invested=stake_amount,
                average_price=current_price
            )
            user_positions[position_key] = position

        # Update market with new share prices for all outcomes
        new_total_stakes = sum(outcome.total_stakes for outcome in market.outcomes)
        for outcome in market.outcomes:
            outcome.share_price = self._calculate_share_price(outcome, new_total_stakes)

    @gl.public.write
    def resolve_market(self, market_id: str) -> None:
        """Resolve a market using AI analysis"""
        if market_id not in self.markets:
            raise Exception("Market not found")
        
        market = self.markets[market_id]
        if market.status != "active":
            raise Exception("Market is not active")

        # Only market creator or contract owner can resolve
        if gl.message.sender_address != market.creator:
            raise Exception("Only market creator can resolve")

        # Use AI to resolve the market
        resolution_result = self._resolve_market_with_ai(market)
        
        if resolution_result["resolved_outcome_id"] is None:
            raise Exception("Market cannot be resolved yet - insufficient data")

        # Update market status
        market.status = "resolved"
        market.resolved_outcome_id = resolution_result["resolved_outcome_id"]
        market.resolution_data = json.dumps(resolution_result)

        # Distribute winnings to users with winning positions
        self._distribute_winnings(market_id, resolution_result["resolved_outcome_id"])

    def _distribute_winnings(self, market_id: str, winning_outcome_id: str) -> None:
        """Distribute winnings to users who bet on the correct outcome"""
        market = self.markets[market_id]
        
        # Calculate total winning stakes
        winning_stakes = u256(0)
        for outcome in market.outcomes:
            if outcome.id == winning_outcome_id:
                winning_stakes = outcome.total_stakes
                break

        if winning_stakes == 0:
            return  # No one won

        # Distribute proportionally to winners
        for user_addr, positions in self.user_positions.items():
            position_key = f"{market_id}_{winning_outcome_id}"
            if position_key in positions:
                position = positions[position_key]
                # Calculate winnings: (user_stake / total_winning_stakes) * total_market_volume
                user_share_ratio = float(position.total_invested) / float(winning_stakes)
                winnings = u256(int(user_share_ratio * float(market.total_volume)))
                
                # Add to user balance
                current_balance = self.user_balances.get(user_addr, u256(0))
                self.user_balances[user_addr] = current_balance + winnings

    @gl.public.write
    def withdraw_balance(self) -> None:
        """Withdraw accumulated winnings"""
        sender = gl.message.sender_address
        balance = self.user_balances.get(sender, u256(0))
        
        if balance == 0:
            raise Exception("No balance to withdraw")
        
        self.user_balances[sender] = u256(0)
        # In a real implementation, you'd transfer the ETH here
        # gl.transfer(sender, balance)

    # View functions
    @gl.public.view
    def get_markets(self, category: str = "", status: str = "") -> List[dict]:
        """Get all markets, optionally filtered by category and status"""
        result = []
        for market in self.markets.values():
            if category and market.category != category:
                continue
            if status and market.status != status:
                continue
                
            market_dict = {
                "id": market.id,
                "title": market.title,
                "description": market.description,
                "category": market.category,
                "creator": market.creator.as_hex,
                "creation_date": market.creation_date,
                "resolution_date": market.resolution_date,
                "status": market.status,
                "total_volume": str(market.total_volume),
                "outcomes": [
                    {
                        "id": outcome.id,
                        "description": outcome.description,
                        "total_stakes": str(outcome.total_stakes),
                        "share_price": str(outcome.share_price)
                    } for outcome in market.outcomes
                ]
            }
            result.append(market_dict)
        
        return result

    @gl.public.view
    def get_market(self, market_id: str) -> dict:
        """Get detailed information about a specific market"""
        if market_id not in self.markets:
            raise Exception("Market not found")
        
        market = self.markets[market_id]
        return {
            "id": market.id,
            "title": market.title,
            "description": market.description,
            "category": market.category,
            "creator": market.creator.as_hex,
            "creation_date": market.creation_date,
            "resolution_date": market.resolution_date,
            "resolution_source": market.resolution_source,
            "status": market.status,
            "total_volume": str(market.total_volume),
            "resolved_outcome_id": market.resolved_outcome_id,
            "resolution_data": market.resolution_data,
            "min_stake": str(market.min_stake),
            "outcomes": [
                {
                    "id": outcome.id,
                    "description": outcome.description,
                    "total_stakes": str(outcome.total_stakes),
                    "share_price": str(outcome.share_price)
                } for outcome in market.outcomes
            ]
        }

    @gl.public.view
    def get_user_positions(self, user_address: str = "") -> List[dict]:
        """Get all positions for a user"""
        addr = Address(user_address) if user_address else gl.message.sender_address
        
        if addr not in self.user_positions:
            return []
        
        positions = []
        for position in self.user_positions[addr].values():
            market = self.markets[position.market_id]
            positions.append({
                "market_id": position.market_id,
                "market_title": market.title,
                "outcome_id": position.outcome_id,
                "shares": str(position.shares),
                "total_invested": str(position.total_invested),
                "average_price": str(position.average_price),
                "market_status": market.status
            })
        
        return positions

    @gl.public.view
    def get_user_balance(self, user_address: str = "") -> str:
        """Get withdrawable balance for a user"""
        addr = Address(user_address) if user_address else gl.message.sender_address
        return str(self.user_balances.get(addr, u256(0)))

    @gl.public.view
    def get_trending_markets(self) -> List[dict]:
        """Get markets with highest activity (volume and recent bets)"""
        # Sort markets by total volume
        market_list = []
        for market in self.markets.values():
            if market.status == "active":
                market_list.append({
                    "id": market.id,
                    "title": market.title,
                    "category": market.category,
                    "total_volume": market.total_volume,
                    "outcomes_count": len(market.outcomes)
                })
        
        # Sort by volume (descending)
        market_list.sort(key=lambda x: x["total_volume"], reverse=True)
        return market_list[:10]  # Top 10 trending markets
