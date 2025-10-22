from gltest import get_contract_factory, default_account
from gltest.helpers import load_fixture
from gltest.assertions import tx_execution_succeeded


def deploy_contract():
    factory = get_contract_factory("PredictionMarket")
    contract = factory.deploy()

    # Get Initial State - should be empty
    markets = contract.get_markets(args=[])
    assert markets == []
    
    trending = contract.get_trending_markets(args=[])
    assert trending == []
    
    return contract


def test_prediction_market_creation():
    """Test creating a new prediction market"""
    contract = load_fixture(deploy_contract)
    
    # Create a simple election market
    result = contract.create_market(
        args=[
            "Who will win the 2025 Election?",  # title
            "Prediction market for US Presidential Election",  # description
            "politics",  # category
            "2025-11-06",  # resolution_date
            "https://www.cnn.com/election/2025/results",  # resolution_source
            ["Democrat", "Republican", "Other"],  # outcomes
            "0.01"  # min_stake_eth
        ]
    )
    
    assert tx_execution_succeeded(result)
    market_id = result.return_value
    assert market_id == "market_1"
    
    # Check that market was created
    markets = contract.get_markets(args=[])
    assert len(markets) == 1
    
    market = markets[0]
    assert market["title"] == "Who will win the 2025 Election?"
    assert market["category"] == "politics"
    assert market["status"] == "active"
    assert len(market["outcomes"]) == 3


def test_prediction_market_betting():
    """Test placing bets on prediction markets"""
    contract = load_fixture(deploy_contract)
    
    # Create a sports market
    result = contract.create_market(
        args=[
            "Super Bowl 2026 Winner",
            "Which team will win Super Bowl 2026?",
            "sports",
            "2026-02-15",
            "https://www.espn.com/nfl/superbowl/",
            ["Chiefs", "Bills", "Ravens", "Other"],
            "0.005"
        ]
    )
    
    assert tx_execution_succeeded(result)
    market_id = result.return_value
    
    # Place a bet on Chiefs
    bet_result = contract.place_bet(
        args=[market_id, "outcome_1"],
        value=1000000000000000000  # 1 ETH in wei
    )
    
    assert tx_execution_succeeded(bet_result)
    
    # Check user positions
    positions = contract.get_user_positions(args=[])
    assert len(positions) == 1
    
    position = positions[0]
    assert position["market_id"] == market_id
    assert position["outcome_id"] == "outcome_1"


def test_multiple_categories():
    """Test creating markets in different categories"""
    contract = load_fixture(deploy_contract)
    
    categories = ["sports", "politics", "entertainment", "economics", "crypto"]
    
    for i, category in enumerate(categories):
        result = contract.create_market(
            args=[
                f"Test Market {i+1}",
                f"A {category} prediction market",
                category,
                "2025-12-31",
                f"https://example.com/{category}",
                ["Yes", "No"],
                "0.01"
            ]
        )
        assert tx_execution_succeeded(result)
    
    # Check all markets created
    markets = contract.get_markets(args=[])
    assert len(markets) == 5
    
    # Test category filtering
    sports_markets = contract.get_markets(args=["sports"])
    assert len(sports_markets) == 1
    assert sports_markets[0]["category"] == "sports"
