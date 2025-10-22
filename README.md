# AI-Powered Prediction Markets on GenLayer
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/license/mit/)
[![Discord](https://dcbadge.vercel.app/api/server/8Jm4v89VAu?compact=true&style=flat)](https://discord.gg/8Jm4v89VAu)
[![Telegram](https://img.shields.io/badge/Telegram--T.svg?style=social&logo=telegram)](https://t.me/genlayer)
[![Twitter](https://img.shields.io/twitter/url/https/twitter.com/yeagerai.svg?style=social&label=Follow%20%40GenLayer)](https://x.com/GenLayer)
[![GitHub star chart](https://img.shields.io/github/stars/yeagerai/genlayer-project-boilerplate?style=social)](https://star-history.com/#yeagerai/genlayer-js)

## 👀 About
This project demonstrates the power of GenLayer's Intelligent Contracts through a comprehensive AI-powered prediction markets platform. Unlike traditional prediction markets, this implementation leverages GenLayer's unique capabilities for web data access, AI-driven analysis, and non-deterministic operations to create truly intelligent markets.

## 🚀 Deployed Contract
**AI-Powered Prediction Markets** is now live on GenLayer Studio!
- **Contract Address:** `0x48eE698ffd6d5c0597bC05A13158b851ECf6F3B5`
- **Network:** GenLayer Studio (Chain ID: 61999)
- **Deployer:** `0x86E95581E41946ED84956433a8a9c836bCbA636c`
- **Studio:** https://studio.genlayer.com

See [DEPLOYMENT.md](./DEPLOYMENT.md) for complete deployment details and usage instructions.

## �📦 What's included
- **Advanced Prediction Market Contract** (`contracts/prediction_market.py`) - Multi-category markets with AI-powered resolution
- **Legacy Football Betting Contract** (`contracts/football_bets.py`) - Original simple betting example
- **Modern Vue.js Frontend** - Comprehensive UI for market discovery, creation, and trading
- **AI Market Maker** - Dynamic pricing based on betting volume and sentiment analysis
- **Multi-Category Support** - Sports, Politics, Entertainment, Economics, Crypto, and more
- **Automated Resolution** - AI analyzes web data to determine market outcomes
- **Comprehensive Tests** - Full test coverage for all contract functionality

## 🛠️ Requirements
- A running GenLayer Studio (Install from [Docs](https://docs.genlayer.com/developers/intelligent-contracts/tooling-setup#using-the-genlayer-studio) or work with the hosted version of [GenLayer Studio](https://studio.genlayer.com/)). If you are working locally, this repository code does not need to be located in the same directory as the Genlayer Studio.
- [GenLayer CLI](https://github.com/genlayerlabs/genlayer-cli) globally installed. To install or update the GenLayer CLI run `npm install -g genlayer`

## 🚀 Steps to run this example

### ⚠️ Security First
Before starting, secure your private keys:
- Copy `keypair.json.example` to `keypair.json` and add your private key
- Never commit `keypair.json` to git (already in `.gitignore`)
- See [DEPLOYMENT.md](./DEPLOYMENT.md) for secure key management

### 1. Deploy the prediction market contract
   Deploy the enhanced prediction market contract from `/contracts/prediction_market.py`:
   1. Choose the network that you want to use (studionet, localnet, or tesnet-*): `genlayer network`
   2. Execute the deploy command `genlayer deploy`. This will deploy the PredictionMarket contract located in `/contracts/prediction_market.py`
   
   **Note**: The deploy script has been updated to use the new prediction market contract instead of the legacy football betting contract.

### 2. Setup the frontend environment
  1. All the content of the dApp is located in the `/app` folder.
  2. Copy the `.env.example` file in the `app` folder and rename it to `.env`, then fill in the values for your configuration. The provided VITE_STUDIO_URL value is the backend of the hosted GenLayer Studio.
  3. Add the deployed contract address to the `/app/.env` under the variable `VITE_CONTRACT_ADDRESS`

### 4. Run the frontend Vue app
   Execute the following commands in your terminal:
   ```shell
   cd app
   npm install
   npm run dev
   ```
   The terminal should display a link to access your frontend app (usually at http://localhost:5173/).
   For more information on the code see [GenLayerJS](https://github.com/yeagerai/genlayer-js).

## 🚀 Key Features

### AI-Powered Market Creation
- **Sentiment Analysis**: AI analyzes market titles and descriptions to suggest optimal initial odds
- **Category Intelligence**: Smart categorization with tailored resolution sources
- **Dynamic Pricing**: Automated market maker adjusts share prices based on betting volume

### Multi-Category Markets
- **Sports**: Football, basketball, esports with real-time data integration
- **Politics**: Elections, policy decisions, geopolitical events
- **Entertainment**: Award shows, TV series outcomes, celebrity predictions
- **Economics**: Market movements, inflation predictions, corporate earnings
- **Crypto**: Price movements, protocol updates, adoption metrics

### Intelligent Resolution
- **Web Data Analysis**: AI fetches and analyzes data from specified sources
- **Consensus Mechanism**: Uses GenLayer's Equivalence Principle for fair resolution
- **Automated Payouts**: Winners automatically receive proportional rewards

### Advanced UI Features
- **Market Discovery**: Browse and filter markets by category and status
- **Position Tracking**: Monitor all your active bets and potential returns
- **Real-time Updates**: Live price updates and market statistics
- **Responsive Design**: Works seamlessly on desktop and mobile devices
   
### 5. Test contracts
1. Install the Python packages listed in the `requirements.txt` file in a virtual environment.
2. Make sure your GenLayer Studio is running. Then execute the following command in your terminal:
   ```shell
   gltest
   ```

## ⚽ How the Football Bets Contract Works

The Football Bets contract allows users to create bets for football matches, resolve those bets, and earn points for correct bets. Here's a breakdown of its main functionalities:

1. Creating Bets:
   - Users can create a bet for a specific football match by providing the game date, team names, and their predicted winner.
   - The contract checks if the game has already finished and if the user has already made a bet for this match.

2. Resolving Bets:
   - After a match has concluded, users can resolve their bets.
   - The contract fetches the actual match result from a specified URL.
   - If the Bet was correct, the user earns a point.

3. Querying Data:
   - Users can retrieve all bets.
   - The contract also allows querying of points, either for all players or for a specific player.

4. Getting Points:
   - Points are awarded for correct bets.
   - Users can check their total points or the points of any player.

## 🧪 Tests

This project includes comprehensive tests for both the legacy football betting system and the new AI-powered prediction markets:

### Prediction Market Tests (`test/test_prediction_market.py`)
1. **Market Creation** - Test creating markets with different categories and configurations
2. **Betting System** - Test placing bets and share price calculations
3. **Multi-Category Support** - Validate all supported market categories
4. **AI Integration** - Test sentiment analysis and market resolution
5. **User Management** - Test positions tracking and balance management

### Legacy Football Betting Tests (`test/test_footbal_bet.py`)
1. Creating a bet
2. Resolving a bet
3. Querying bets for a player
4. Querying points for a player

To run the tests:
```bash
# Install dependencies
pip install -r requirements.txt

# Run all tests (requires GenLayer Studio running on localhost:4000)
gltest
```

## 📖 Usage Examples

### Creating Your First Market

1. **Connect Wallet**: Click "Connect Wallet" to create a new GenLayer account
2. **Choose Template**: Browse market templates or create from scratch
3. **Fill Details**: Add title, description, outcomes, and resolution source
4. **Deploy**: Submit the transaction to create your market

### Example Market Creation (JavaScript)
```javascript
import { GenLayerClient } from './services/genlayer.js'

// Create a simple yes/no market
const marketId = await GenLayerClient.createMarket({
  title: "Will Bitcoin reach $100K in 2025?",
  description: "Market resolves based on Bitcoin price at end of 2025",
  category: "crypto",
  resolution_date: "2025-12-31",
  resolution_source: "https://coinmarketcap.com/",
  outcomes: ["Yes", "No"],
  min_stake_eth: "0.01"
})
```

### Placing Bets
```javascript
// Bet 0.1 ETH on "Yes" outcome
await GenLayerClient.placeBet(marketId, "outcome_1", "100000000000000000")
```

### Market Resolution (AI-Powered)
```javascript
// Markets resolve automatically using AI analysis of web data
await GenLayerClient.resolveMarket(marketId)
```

## 🎯 Market Categories

### Sports Markets
- **Football**: NFL, college football, international soccer
- **Basketball**: NBA, NCAA, international leagues
- **Other Sports**: Baseball, hockey, tennis, esports

### Political Markets
- **Elections**: Presidential, congressional, local elections
- **Policy**: Legislative votes, regulatory decisions
- **International**: Brexit, trade deals, diplomatic events

### Entertainment Markets
- **Awards**: Oscars, Emmys, Grammy predictions
- **Box Office**: Movie performance, streaming success
- **TV/Streaming**: Series renewals, ratings predictions

### Economic Markets
- **Stock Performance**: Individual stocks, indices, sectors
- **Economic Indicators**: GDP, inflation, employment
- **Corporate**: Earnings, mergers, product launches

### Cryptocurrency Markets
- **Price Predictions**: Bitcoin, Ethereum, altcoins
- **Protocol Updates**: Hard forks, major releases
- **Adoption Metrics**: Institutional adoption, regulatory approval


## 🤖 AI-Powered Features

### Intelligent Market Analysis
- **Sentiment Analysis**: AI evaluates market sentiment and suggests optimal initial odds
- **Category-Specific Intelligence**: Tailored analysis for sports, politics, entertainment, etc.
- **Risk Assessment**: Automated evaluation of market volatility and complexity
- **Dynamic Pricing**: Share prices adjust automatically based on betting volume and AI analysis

### Automated Resolution
- **Web Data Integration**: AI fetches and analyzes data from specified sources
- **Multi-Source Verification**: Cross-references multiple data sources for accuracy
- **Consensus Mechanism**: Uses GenLayer's Equivalence Principle for fair resolution
- **Evidence Documentation**: Provides clear reasoning for resolution decisions

### Smart Market Making
- **Volume-Based Pricing**: Prices adjust based on betting activity
- **Liquidity Optimization**: Maintains healthy market liquidity
- **Anti-Manipulation**: Detects and prevents market manipulation attempts

## 🛠️ Technical Architecture

### Smart Contract (`contracts/prediction_market.py`)
- Written in Python for GenLayer's Intelligent Contract platform
- Leverages GenLayer's LLM integration for AI-powered analysis
- Web data access for real-world information integration
- Non-deterministic operations for complex decision making

### Frontend (`app/src/`)
- Modern Vue.js 3 application with Composition API
- Responsive design with Tailwind CSS
- Real-time market updates and position tracking
- Integrated wallet management with GenLayerJS

### AI Integration
- Category-specific market analysis prompts
- Automated data fetching and parsing
- Consensus-based resolution system
- Market sentiment and volatility assessment

## 🚀 Future Enhancements

- **Advanced Trading**: Limit orders, stop losses, market making
- **Social Features**: Market discussions, follower systems, leaderboards
- **Mobile App**: Native iOS and Android applications
- **API Integration**: Real-time data feeds for sports, finance, and news
- **Governance Token**: Community-driven platform governance
- **Cross-Chain Support**: Multi-blockchain market creation and settlement

## 💬 Community
Connect with the GenLayer community to discuss, collaborate, and share insights:
- **[Discord Channel](https://discord.gg/8Jm4v89VAu)**: Our primary hub for discussions, support, and announcements.
- **[Telegram Group](https://t.me/genlayer)**: For more informal chats and quick updates.

Your continuous feedback drives better product development. Please engage with us regularly to test, discuss, and improve GenLayer.

## 📖 Documentation
For detailed information on how to use GenLayerJS SDK, please refer to our [documentation](https://docs.genlayer.com/).

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
