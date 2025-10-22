<template>
  <div class="min-h-screen bg-gray-100 text-gray-900">
    <header class="bg-white shadow flex justify-between">
      <div class="max-w-7xl py-6 px-4 sm:px-6 lg:px-8">
        <h1 class="text-3xl font-bold text-gray-900">GenLayer Prediction Markets</h1>
        <p class="text-gray-600">AI-Powered Decentralized Predictions</p>
      </div>
      <div class="max-w-7xl py-6 px-4 sm:px-6 lg:px-8 text-right">
        <div v-if="!userAddress">
          <button
            @click="createUserAccount"
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >
            Connect Wallet
          </button>
        </div>
        <div v-else>
          <p class="text-lg">Address: <Address :address="userAddress" /></p>
          <p class="text-lg">Balance: {{ userBalance }} ETH</p>
          <button
            @click="disconnectUserAccount"
            class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
          >
            Disconnect
          </button>
        </div>
      </div>
    </header>
    
    <main class="mx-auto py-6 sm:px-6 lg:px-8">
      <!-- Navigation Tabs -->
      <div class="mb-8">
        <nav class="flex space-x-8" aria-label="Tabs">
          <button
            v-for="tab in tabs"
            :key="tab.id"
            @click="currentTab = tab.id"
            :class="[
              tab.id === currentTab
                ? 'border-blue-500 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300',
              'whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm'
            ]"
          >
            {{ tab.name }}
          </button>
        </nav>
      </div>

      <!-- Market Discovery Tab -->
      <div v-if="currentTab === 'discover'" class="space-y-8">
        <!-- Category Filter -->
        <div class="bg-white p-6 shadow rounded-lg">
          <h3 class="text-lg font-medium mb-4">Filter Markets</h3>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="category in categories"
              :key="category"
              @click="selectedCategory = selectedCategory === category ? '' : category"
              :class="[
                selectedCategory === category
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-200 text-gray-700 hover:bg-gray-300',
                'px-3 py-2 rounded-md text-sm font-medium'
              ]"
            >
              {{ category.charAt(0).toUpperCase() + category.slice(1) }}
            </button>
          </div>
        </div>

        <!-- Trending Markets -->
        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
          <div class="px-4 py-5 sm:px-6 flex justify-between items-center">
            <div>
              <h2 class="text-lg leading-6 font-medium text-gray-900">
                {{ selectedCategory ? selectedCategory.charAt(0).toUpperCase() + selectedCategory.slice(1) + ' Markets' : 'All Markets' }}
              </h2>
              <p class="text-sm text-gray-600">{{ filteredMarkets.length }} active predictions</p>
            </div>
            <button
              @click="showCreateModal = true"
              class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded"
            >
              Create Market
            </button>
          </div>
          
          <!-- Markets Grid -->
          <div class="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            <div
              v-for="market in filteredMarkets"
              :key="market.id"
              class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow cursor-pointer"
              @click="selectedMarket = market"
            >
              <div class="flex justify-between items-start mb-3">
                <span :class="categoryColors[market.category]" class="px-2 py-1 text-xs font-semibold rounded-full">
                  {{ market.category }}
                </span>
                <span class="text-xs text-gray-500">{{ market.total_volume }} ETH</span>
              </div>
              
              <h3 class="font-medium text-gray-900 mb-2 line-clamp-2">{{ market.title }}</h3>
              <p class="text-sm text-gray-600 mb-3 line-clamp-2">{{ market.description }}</p>
              
              <!-- Outcomes Preview -->
              <div class="space-y-1 mb-3">
                <div
                  v-for="outcome in market.outcomes.slice(0, 2)"
                  :key="outcome.id"
                  class="flex justify-between text-xs"
                >
                  <span>{{ outcome.description }}</span>
                  <span class="font-medium">{{ formatPrice(outcome.share_price) }} ETH</span>
                </div>
                <div v-if="market.outcomes.length > 2" class="text-xs text-gray-500">
                  +{{ market.outcomes.length - 2 }} more options
                </div>
              </div>
              
              <div class="flex justify-between items-center text-xs text-gray-500">
                <span>Resolves: {{ market.resolution_date }}</span>
                <span class="font-medium text-blue-600">View Details →</span>
              </div>
            </div>
          </div>
          
          <!-- Empty State -->
          <div v-if="filteredMarkets.length === 0" class="text-center py-12">
            <div class="text-gray-500 mb-4">
              <svg class="mx-auto h-12 w-12" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
            </div>
            <h3 class="text-lg font-medium text-gray-900 mb-2">No Markets Found</h3>
            <p class="text-gray-600 mb-4">
              {{ selectedCategory ? `No ${selectedCategory} markets available` : 'No active prediction markets' }}
            </p>
            <button
              @click="showCreateModal = true"
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >
              Create First Market
            </button>
          </div>
        </div>
      </div>

      <!-- My Positions Tab -->
      <div v-if="currentTab === 'positions'" class="space-y-8">
        <div class="bg-white shadow overflow-hidden sm:rounded-lg">
          <div class="px-4 py-5 sm:px-6">
            <h2 class="text-lg leading-6 font-medium text-gray-900">My Positions</h2>
            <p class="text-sm text-gray-600">{{ userPositions.length }} active positions</p>
          </div>
          
          <div class="border-t border-gray-200">
            <table v-if="userPositions.length > 0" class="min-w-full divide-y divide-gray-200">
              <thead class="bg-gray-50">
                <tr>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Market</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Position</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Shares</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Invested</th>
                  <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
                </tr>
              </thead>
              <tbody class="bg-white divide-y divide-gray-200">
                <tr v-for="position in userPositions" :key="position.market_id + position.outcome_id">
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm font-medium text-gray-900">{{ position.market_title }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <div class="text-sm text-gray-900">{{ getOutcomeDescription(position) }}</div>
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ formatShares(position.shares) }}
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                    {{ formatPrice(position.total_invested) }} ETH
                  </td>
                  <td class="px-6 py-4 whitespace-nowrap">
                    <span :class="position.market_status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'" class="px-2 inline-flex text-xs leading-5 font-semibold rounded-full">
                      {{ position.market_status }}
                    </span>
                  </td>
                </tr>
              </tbody>
            </table>
            
            <div v-else class="text-center py-12">
              <p class="text-gray-600">No positions yet. Start by betting on a market!</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Market Detail Modal -->
      <div v-if="selectedMarket" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
        <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
          <div class="mt-3">
            <div class="flex justify-between items-start mb-4">
              <h3 class="text-lg font-medium text-gray-900">{{ selectedMarket.title }}</h3>
              <button @click="selectedMarket = null" class="text-gray-400 hover:text-gray-600">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <div class="mb-4">
              <span :class="categoryColors[selectedMarket.category]" class="px-2 py-1 text-xs font-semibold rounded-full">
                {{ selectedMarket.category }}
              </span>
            </div>
            
            <p class="text-gray-600 mb-6">{{ selectedMarket.description }}</p>
            
            <div class="grid grid-cols-2 gap-4 mb-6 text-sm">
              <div><strong>Total Volume:</strong> {{ selectedMarket.total_volume }} ETH</div>
              <div><strong>Resolution Date:</strong> {{ selectedMarket.resolution_date }}</div>
              <div><strong>Min Stake:</strong> {{ formatPrice(selectedMarket.min_stake) }} ETH</div>
              <div><strong>Status:</strong> {{ selectedMarket.status }}</div>
            </div>
            
            <h4 class="font-medium mb-3">Outcomes</h4>
            <div class="space-y-3 mb-6">
              <div
                v-for="outcome in selectedMarket.outcomes"
                :key="outcome.id"
                class="flex justify-between items-center p-3 border rounded-lg hover:bg-gray-50"
              >
                <div class="flex-1">
                  <div class="font-medium">{{ outcome.description }}</div>
                  <div class="text-sm text-gray-600">{{ formatPrice(outcome.share_price) }} ETH per share</div>
                </div>
                <button
                  @click="placeBet(selectedMarket.id, outcome.id)"
                  :disabled="!userAddress"
                  class="bg-blue-500 hover:bg-blue-700 disabled:bg-gray-300 text-white font-bold py-2 px-4 rounded"
                >
                  Buy Shares
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Create Market Modal -->
      <div v-if="showCreateModal" class="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
        <div class="relative top-20 mx-auto p-5 border w-11/12 md:w-3/4 lg:w-1/2 shadow-lg rounded-md bg-white">
          <div class="mt-3">
            <div class="flex justify-between items-start mb-4">
              <h3 class="text-lg font-medium text-gray-900">Create Prediction Market</h3>
              <button @click="showCreateModal = false" class="text-gray-400 hover:text-gray-600">
                <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
            
            <!-- Market Templates -->
            <MarketTemplates @useTemplate="useMarketTemplate" class="mb-6" />
            
            <form @submit.prevent="createMarket" class="space-y-4">
              <div>
                <label class="block text-sm font-medium text-gray-700">Title</label>
                <input v-model="newMarket.title" type="text" required class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2">
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">Description</label>
                <textarea v-model="newMarket.description" required class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 h-20"></textarea>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">Category</label>
                <select v-model="newMarket.category" required class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2">
                  <option value="">Select category</option>
                  <option v-for="category in categories" :key="category" :value="category">
                    {{ category.charAt(0).toUpperCase() + category.slice(1) }}
                  </option>
                </select>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">Resolution Date</label>
                <input v-model="newMarket.resolution_date" type="date" required class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2">
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">Resolution Source URL</label>
                <input v-model="newMarket.resolution_source" type="url" required class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2">
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">Outcomes (one per line)</label>
                <textarea v-model="newMarket.outcomes" required placeholder="Yes&#10;No" class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2 h-20"></textarea>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-gray-700">Minimum Stake (ETH)</label>
                <input v-model="newMarket.min_stake" type="number" step="0.001" min="0.001" required class="mt-1 block w-full border border-gray-300 rounded-md px-3 py-2">
              </div>
              
              <div class="flex justify-end space-x-3">
                <button type="button" @click="showCreateModal = false" class="bg-gray-300 hover:bg-gray-400 text-gray-800 font-bold py-2 px-4 rounded">
                  Cancel
                </button>
                <button type="submit" :disabled="!userAddress || creatingMarket" class="bg-green-500 hover:bg-green-700 disabled:bg-gray-300 text-white font-bold py-2 px-4 rounded">
                  {{ creatingMarket ? 'Creating...' : 'Create Market' }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { GenLayerClient } from '../services/genlayer.js'
import Address from './Address.vue'
import MarketTemplates from './MarketTemplates.vue'

// Reactive state
const currentTab = ref('discover')
const selectedCategory = ref('')
const selectedMarket = ref(null)
const showCreateModal = ref(false)
const creatingMarket = ref(false)

const userAddress = ref('')
const userBalance = ref('0')
const markets = ref([])
const userPositions = ref([])

const tabs = [
  { id: 'discover', name: 'Discover Markets' },
  { id: 'positions', name: 'My Positions' }
]

const categories = ['sports', 'politics', 'entertainment', 'economics', 'crypto', 'other']

const categoryColors = {
  sports: 'bg-blue-100 text-blue-800',
  politics: 'bg-red-100 text-red-800',
  entertainment: 'bg-purple-100 text-purple-800',
  economics: 'bg-green-100 text-green-800',
  crypto: 'bg-yellow-100 text-yellow-800',
  other: 'bg-gray-100 text-gray-800'
}

const newMarket = ref({
  title: '',
  description: '',
  category: '',
  resolution_date: '',
  resolution_source: '',
  outcomes: '',
  min_stake: '0.01'
})

// Computed
const filteredMarkets = computed(() => {
  if (!selectedCategory.value) return markets.value
  return markets.value.filter(market => market.category === selectedCategory.value)
})

// Methods
const formatPrice = (wei) => {
  return (parseFloat(wei) / 1e18).toFixed(4)
}

const formatShares = (shares) => {
  return (parseFloat(shares) / 1e18).toFixed(2)
}

const getOutcomeDescription = (position) => {
  const market = markets.value.find(m => m.id === position.market_id)
  if (!market) return 'Unknown'
  const outcome = market.outcomes.find(o => o.id === position.outcome_id)
  return outcome ? outcome.description : 'Unknown'
}

const createUserAccount = async () => {
  try {
    const address = await GenLayerClient.createAccount()
    userAddress.value = address
    await loadData()
  } catch (error) {
    console.error('Error creating account:', error)
    alert('Failed to create account')
  }
}

const disconnectUserAccount = () => {
  userAddress.value = ''
  userBalance.value = '0'
  userPositions.value = []
}

const loadData = async () => {
  try {
    // Load markets
    const marketsData = await GenLayerClient.getMarkets()
    markets.value = marketsData
    
    // Load user positions if connected
    if (userAddress.value) {
      const positionsData = await GenLayerClient.getUserPositions(userAddress.value)
      userPositions.value = positionsData
      
      const balance = await GenLayerClient.getUserBalance(userAddress.value)
      userBalance.value = formatPrice(balance)
    }
  } catch (error) {
    console.error('Error loading data:', error)
  }
}

const createMarket = async () => {
  if (!userAddress.value) {
    alert('Please connect your wallet first')
    return
  }
  
  creatingMarket.value = true
  
  try {
    const outcomes = newMarket.value.outcomes.split('\n').filter(o => o.trim())
    
    if (outcomes.length < 2) {
      alert('Please provide at least 2 outcomes')
      return
    }
    
    const marketId = await GenLayerClient.createMarket({
      title: newMarket.value.title,
      description: newMarket.value.description,
      category: newMarket.value.category,
      resolution_date: newMarket.value.resolution_date,
      resolution_source: newMarket.value.resolution_source,
      outcomes: outcomes,
      min_stake_eth: newMarket.value.min_stake
    })
    
    alert(`Market created successfully! ID: ${marketId}`)
    
    // Reset form and reload data
    newMarket.value = {
      title: '',
      description: '',
      category: '',
      resolution_date: '',
      resolution_source: '',
      outcomes: '',
      min_stake: '0.01'
    }
    showCreateModal.value = false
    await loadData()
    
  } catch (error) {
    console.error('Error creating market:', error)
    alert('Failed to create market: ' + error.message)
  } finally {
    creatingMarket.value = false
  }
}

const useMarketTemplate = (template) => {
  // Fill form with template data
  newMarket.value = {
    title: template.title,
    description: template.description,
    category: template.category,
    resolution_date: '2025-12-31', // Default future date
    resolution_source: template.resolution_source,
    outcomes: template.outcomes.join('\n'),
    min_stake: template.min_stake
  }
}

const placeBet = async (marketId, outcomeId) => {
  if (!userAddress.value) {
    alert('Please connect your wallet first')
    return
  }
  
  const amount = prompt('Enter bet amount in ETH:', '0.1')
  if (!amount || isNaN(amount) || parseFloat(amount) <= 0) {
    return
  }
  
  try {
    const weiAmount = Math.floor(parseFloat(amount) * 1e18).toString()
    
    await GenLayerClient.placeBet(marketId, outcomeId, weiAmount)
    
    alert('Bet placed successfully!')
    await loadData()
    selectedMarket.value = null
    
  } catch (error) {
    console.error('Error placing bet:', error)
    alert('Failed to place bet: ' + error.message)
  }
}

// Lifecycle
onMounted(() => {
  loadData()
  
  // Auto-refresh data every 30 seconds
  setInterval(loadData, 30000)
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
