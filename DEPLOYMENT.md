# GenLayer Prediction Market - Deployment Guide

## 🎉 Production Deployment

### Live Contract Information
- **Contract Address:** `0x48eE698ffd6d5c0597bC05A13158b851ECf6F3B5`
- **Network:** GenLayer Studio
- **Chain ID:** 61999
- **RPC URL:** https://studio.genlayer.com/api
- **Studio Dashboard:** https://studio.genlayer.com
- **Deployed:** October 23, 2025

## 📋 Contract Features

### Multi-Category Prediction Markets
The production contract supports multiple prediction categories:
- **Sports** - Sports events, tournaments, championships
- **Politics** - Elections, policy outcomes, governance
- **Entertainment** - Awards, box office, streaming metrics
- **Economics** - Market predictions, GDP, inflation
- **Crypto** - Token prices, protocol launches, TVL milestones

### AI-Powered Features
1. **Automated Market Resolution** - AI analyzes web data to determine outcomes
2. **Dynamic Pricing** - Automated market maker adjusts odds based on volume
3. **Sentiment Analysis** - AI evaluates market sentiment from multiple sources
4. **Data Validation** - Equivalence principle ensures consensus on outcomes

### Key Contract Methods

#### Create a Market
```python
create_market(
    title: str,
    description: str,
    category: str,  # sports, politics, entertainment, economics, crypto
    outcomes: List[str],  # e.g., ["Yes", "No"] or ["Team A", "Team B"]
    resolution_date: str,
    resolution_source: str,
    min_stake: u256
) -> str  # Returns market_id
```

#### Place a Bet
```python
place_bet(
    market_id: str,
    outcome_id: str,
    stake: u256
) -> dict
```

#### Resolve Market
```python
resolve_market(market_id: str) -> dict
```

#### Query Methods (Free)
```python
get_market(market_id: str) -> dict
get_all_markets() -> dict
get_user_positions(user_address: Address) -> dict
get_market_stats() -> dict
```

## 🚀 Quick Start

## Prerequisites

1. **Node.js** (v18 or higher)
2. **GenLayer Studio Account** - https://studio.genlayer.com
3. **Private Key** - Store securely in `keypair.json` (never commit this file!)

### Setting Up Private Key

Create a `keypair.json` file in the project root:

```json
{
  "private_key": "YOUR_PRIVATE_KEY_HERE",
  "address": "YOUR_WALLET_ADDRESS_HERE"
}
```

⚠️ **SECURITY WARNING**: 
- The `keypair.json` file is already in `.gitignore`
- NEVER commit private keys to git
- Use `keypair.json.example` as a template for others
- Consider using environment variables for production deployments

## Installation

### 1. Environment Setup
```bash
# Create .env file with your private key
echo "GENLAYER_PRIVATE_KEY=your_private_key_here" > .env
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Deploy Contract (if redeploying)
```bash
export GENLAYER_PRIVATE_KEY=$(cat .env | grep GENLAYER_PRIVATE_KEY | cut -d'=' -f2)
node deploy.mjs
```

### 4. Run Frontend
```bash
cd app
npm install
npm run dev
```

## 🔧 Frontend Integration

Update `app/src/services/genlayer.js` with the deployed contract address:

```javascript
const PREDICTION_MARKET_ADDRESS = '0x48eE698ffd6d5c0597bC05A13158b851ECf6F3B5';

const NETWORK_CONFIG = {
  id: 61999,
  name: 'GenLayer Studio',
  rpcUrl: 'https://studio.genlayer.com/api'
};
```

## 📁 Project Structure

```
genlayer-builder/
├── contracts/
│   ├── prediction_market.py       # Production contract (deployed)
│   ├── market_templates.py        # Market category templates
│   └── example_markets.py         # Example market configurations
├── app/
│   ├── src/
│   │   ├── components/
│   │   │   ├── PredictionMarkets.vue
│   │   │   └── MarketTemplates.vue
│   │   └── services/
│   │       └── genlayer.js
│   └── package.json
├── deploy.mjs                     # Deployment script
└── deployed_contract.json         # Deployment info
```

## 🧪 Testing the Contract

### Using GenLayer Studio
1. Visit https://studio.genlayer.com
2. Connect your wallet
3. Use contract address: `0x48eE698ffd6d5c0597bC05A13158b851ECf6F3B5`

### Example: Create a Market
```python
# Create a crypto price prediction market
market_id = contract.create_market(
    title="Will Bitcoin reach $100k in 2025?",
    description="Market resolves YES if BTC reaches $100,000 on any major exchange before Dec 31, 2025",
    category="crypto",
    outcomes=["Yes", "No"],
    resolution_date="2025-12-31",
    resolution_source="https://www.coindesk.com/price/bitcoin",
    min_stake=1000000000000000  # 0.001 GEN
)
```

### Example: Place a Bet
```python
# Bet on "Yes" outcome
receipt = contract.place_bet(
    market_id=market_id,
    outcome_id="Yes",
    stake=10000000000000000  # 0.01 GEN
)
```

## 🔒 Security Notes

- Private keys are stored in `.env` (never commit to git)
- All transactions require validator consensus
- AI resolution uses equivalence principle for fairness
- Markets can only be resolved once
- Stakes are locked until market resolution

## 📊 Network Information

### GenLayer Studio
- **Purpose:** Development and testing environment
- **Speed:** Fast consensus (~30-120 seconds)
- **Cost:** Free testnet GEN tokens
- **Persistence:** Data may be reset periodically

### Future: Production Testnet
- **Network:** GenLayer Asimov Testnet
- **Chain ID:** 4221
- **RPC:** https://genlayer-testnet.rpc.caldera.xyz/http
- **Explorer:** https://genlayer-testnet.explorer.caldera.xyz

## 🆘 Troubleshooting

### Transaction Taking Too Long
GenLayer Intelligent Contracts require validator consensus which takes 30-120 seconds. Be patient!

### Deployment Fails
1. Check your account has GEN tokens
2. Verify network connectivity
3. Ensure private key is correctly set in `.env`
4. Try deploying to Studio network first

### Contract Interaction Errors
1. Verify contract address is correct
2. Ensure you're connected to the right network (Chain ID: 61999)
3. Check method parameters match the contract schema
4. Confirm you have sufficient GEN for gas

## 📚 Additional Resources

- **GenLayer Documentation:** https://docs.genlayer.com
- **GenLayer Studio:** https://studio.genlayer.com
- **GitHub Repository:** https://github.com/genlayerlabs
- **Discord Community:** https://discord.gg/8Jm4v89VAu

## 📝 License

MIT License - See LICENSE file for details
