import { createClient, createAccount as createGenLayerAccount, generatePrivateKey } from "genlayer-js";
import { studionet } from "genlayer-js/chains";

const accountPrivateKey = localStorage.getItem("accountPrivateKey")
  ? localStorage.getItem("accountPrivateKey")
  : null;
export const account = accountPrivateKey ? createGenLayerAccount(accountPrivateKey) : null;

export const createAccount = () => {
  const newAccountPrivateKey = generatePrivateKey();
  localStorage.setItem("accountPrivateKey", newAccountPrivateKey);
  return createGenLayerAccount(newAccountPrivateKey);
};

export const removeAccount = () => {
  localStorage.removeItem("accountPrivateKey");
};

export const client = createClient({ chain: studionet, account });

// Contract configuration
const CONTRACT_ADDRESS = import.meta.env.VITE_CONTRACT_ADDRESS;

export const GenLayerClient = {
  async createAccount() {
    const newAccount = createAccount();
    return newAccount.address;
  },

  // New Prediction Market Methods
  async createMarket(marketData) {
    const currentClient = createClient({ 
      chain: studionet, 
      account: account || createAccount() 
    });
    
    const result = await currentClient.writeContract({
      address: CONTRACT_ADDRESS,
      functionName: "create_market",
      args: [
        marketData.title,
        marketData.description,
        marketData.category,
        marketData.resolution_date,
        marketData.resolution_source,
        marketData.outcomes,
        marketData.min_stake_eth
      ]
    });
    return result;
  },

  async placeBet(marketId, outcomeId, amount) {
    const currentClient = createClient({ 
      chain: studionet, 
      account: account || createAccount() 
    });
    
    const result = await currentClient.writeContract({
      address: CONTRACT_ADDRESS,
      functionName: "place_bet",
      args: [marketId, outcomeId],
      value: BigInt(amount)
    });
    return result;
  },

  async resolveMarket(marketId) {
    const currentClient = createClient({ 
      chain: studionet, 
      account: account || createAccount() 
    });
    
    const result = await currentClient.writeContract({
      address: CONTRACT_ADDRESS,
      functionName: "resolve_market",
      args: [marketId]
    });
    return result;
  },

  async withdrawBalance() {
    const currentClient = createClient({ 
      chain: studionet, 
      account: account || createAccount() 
    });
    
    const result = await currentClient.writeContract({
      address: CONTRACT_ADDRESS,
      functionName: "withdraw_balance",
      args: []
    });
    return result;
  },

  async getMarkets(category = "", status = "") {
    const currentClient = createClient({ 
      chain: studionet, 
      account: account || createAccount() 
    });
    
    const result = await currentClient.readContract({
      address: CONTRACT_ADDRESS,
      functionName: "get_markets",
      args: [category, status]
    });
    return result;
  },

  async getMarket(marketId) {
    const currentClient = createClient({ 
      chain: studionet, 
      account: account || createAccount() 
    });
    
    const result = await currentClient.readContract({
      address: CONTRACT_ADDRESS,
      functionName: "get_market",
      args: [marketId]
    });
    return result;
  },

  async getUserPositions(userAddress = "") {
    const currentClient = createClient({ 
      chain: studionet, 
      account: account || createAccount() 
    });
    
    const result = await currentClient.readContract({
      address: CONTRACT_ADDRESS,
      functionName: "get_user_positions",
      args: [userAddress]
    });
    return result;
  },

  async getUserBalance(userAddress = "") {
    const currentClient = createClient({ 
      chain: studionet, 
      account: account || createAccount() 
    });
    
    const result = await currentClient.readContract({
      address: CONTRACT_ADDRESS,
      functionName: "get_user_balance",
      args: [userAddress]
    });
    return result;
  },

  async getTrendingMarkets() {
    const currentClient = createClient({ 
      chain: studionet, 
      account: account || createAccount() 
    });
    
    const result = await currentClient.readContract({
      address: CONTRACT_ADDRESS,
      functionName: "get_trending_markets",
      args: []
    });
    return result;
  },

  // Legacy Football Betting Methods (for backwards compatibility)
  async createBet(gameDate, team1, team2, predictedWinner) {
    const currentClient = createClient({ 
      chain: studionet, 
      account: account || createAccount() 
    });
    
    const result = await currentClient.writeContract({
      address: CONTRACT_ADDRESS,
      functionName: "create_bet",
      args: [gameDate, team1, team2, predictedWinner]
    });
    return result;
  },

  async resolveBet(betId) {
    const currentClient = createClient({ 
      chain: studionet, 
      account: account || createAccount() 
    });
    
    const result = await currentClient.writeContract({
      address: CONTRACT_ADDRESS,
      functionName: "resolve_bet",
      args: [betId]
    });
    return result;
  },

  async getBets() {
    const currentClient = createClient({ 
      chain: studionet, 
      account: account || createAccount() 
    });
    
    const result = await currentClient.readContract({
      address: CONTRACT_ADDRESS,
      functionName: "get_bets",
      args: []
    });
    return result;
  },

  async getPoints() {
    const currentClient = createClient({ 
      chain: studionet, 
      account: account || createAccount() 
    });
    
    const result = await currentClient.readContract({
      address: CONTRACT_ADDRESS,
      functionName: "get_points",
      args: []
    });
    return result;
  },

  async getPlayerPoints(playerAddress) {
    const currentClient = createClient({ 
      chain: studionet, 
      account: account || createAccount() 
    });
    
    const result = await currentClient.readContract({
      address: CONTRACT_ADDRESS,
      functionName: "get_player_points",
      args: [playerAddress]
    });
    return result;
  },
};
