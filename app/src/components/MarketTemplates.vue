<template>
  <div class="bg-white shadow rounded-lg p-6">
    <div class="flex justify-between items-center mb-4">
      <h3 class="text-lg font-medium text-gray-900">Market Templates</h3>
      <button
        @click="showTemplates = !showTemplates"
        class="text-blue-600 hover:text-blue-800 text-sm"
      >
        {{ showTemplates ? 'Hide' : 'Show' }} Examples
      </button>
    </div>
    
    <div v-if="showTemplates" class="space-y-4">
      <!-- Category Selector -->
      <div class="flex flex-wrap gap-2 mb-4">
        <button
          v-for="category in Object.keys(exampleMarkets)"
          :key="category"
          @click="selectedCategory = category"
          :class="[
            selectedCategory === category
              ? 'bg-blue-500 text-white'
              : 'bg-gray-200 text-gray-700 hover:bg-gray-300',
            'px-3 py-1 rounded-md text-sm font-medium'
          ]"
        >
          {{ formatCategory(category) }}
        </button>
      </div>
      
      <!-- Market Examples -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div
          v-for="(market, index) in exampleMarkets[selectedCategory]"
          :key="`${selectedCategory}-${index}`"
          class="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
        >
          <div class="flex justify-between items-start mb-2">
            <h4 class="font-medium text-gray-900 text-sm">{{ market.title }}</h4>
            <button
              @click="useTemplate(market)"
              class="text-xs bg-green-500 hover:bg-green-600 text-white px-2 py-1 rounded"
            >
              Use Template
            </button>
          </div>
          
          <p class="text-xs text-gray-600 mb-2 line-clamp-2">{{ market.description }}</p>
          
          <div class="space-y-1 text-xs">
            <div><strong>Outcomes:</strong> {{ market.outcomes.slice(0, 3).join(', ') }}
              <span v-if="market.outcomes.length > 3" class="text-gray-500">+{{ market.outcomes.length - 3 }} more</span>
            </div>
            <div><strong>Min Stake:</strong> {{ market.min_stake }} ETH</div>
          </div>
        </div>
      </div>
      
      <!-- Quick Create Buttons -->
      <div class="border-t pt-4 mt-4">
        <h4 class="font-medium text-gray-700 mb-2">Quick Create Popular Markets:</h4>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="quickMarket in quickCreateMarkets"
            :key="quickMarket.title"
            @click="useTemplate(quickMarket)"
            class="bg-blue-100 hover:bg-blue-200 text-blue-800 px-3 py-2 rounded-md text-sm"
          >
            {{ quickMarket.title }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue'

const emit = defineEmits(['useTemplate'])
const showTemplates = ref(false)
const selectedCategory = ref('sports')

const exampleMarkets = {
  sports: [
    {
      title: "Super Bowl 2026 Winner",
      description: "Which team will win Super Bowl 2026? Market resolves based on official NFL results.",
      category: "sports",
      resolution_source: "https://www.nfl.com/super-bowl/",
      outcomes: ["Kansas City Chiefs", "Buffalo Bills", "Baltimore Ravens", "San Francisco 49ers", "Other AFC Team", "Other NFC Team"],
      min_stake: "0.01"
    },
    {
      title: "NBA 2025 Championship",
      description: "Predict the NBA Championship winner for the 2024-25 season.",
      category: "sports",
      resolution_source: "https://www.nba.com/playoffs/",
      outcomes: ["Boston Celtics", "Golden State Warriors", "Los Angeles Lakers", "Denver Nuggets", "Other Team"],
      min_stake: "0.005"
    },
    {
      title: "Premier League 2025 Champion",
      description: "Which team will win the 2024-25 Premier League title?",
      category: "sports",
      resolution_source: "https://www.premierleague.com/",
      outcomes: ["Manchester City", "Arsenal", "Liverpool", "Chelsea", "Manchester United", "Other"],
      min_stake: "0.01"
    }
  ],
  
  politics: [
    {
      title: "US Presidential Election 2028",
      description: "Who will win the 2028 US Presidential Election?",
      category: "politics",
      resolution_source: "https://apnews.com/",
      outcomes: ["Democratic Candidate", "Republican Candidate", "Third Party/Independent"],
      min_stake: "0.02"
    },
    {
      title: "Next Federal Reserve Rate Decision",
      description: "What will the Federal Reserve do with interest rates at the next FOMC meeting?",
      category: "politics",
      resolution_source: "https://www.federalreserve.gov/",
      outcomes: ["Raise Rates", "Lower Rates", "Keep Rates Unchanged"],
      min_stake: "0.01"
    }
  ],
  
  entertainment: [
    {
      title: "Oscars 2026 Best Picture",
      description: "Which film will win Best Picture at the 2026 Academy Awards?",
      category: "entertainment",
      resolution_source: "https://oscar.go.com/",
      outcomes: ["Top Drama Film", "Top Action/Sci-Fi Film", "Top Comedy Film", "Documentary", "International Film", "Other"],
      min_stake: "0.005"
    },
    {
      title: "Netflix Series Renewal",
      description: "Will Netflix renew Stranger Things for another season in 2025?",
      category: "entertainment",
      resolution_source: "https://variety.com/",
      outcomes: ["Renewed", "Cancelled", "No Decision by End of Year"],
      min_stake: "0.01"
    }
  ],
  
  crypto: [
    {
      title: "Bitcoin Price End of 2025",
      description: "What will Bitcoin's price be at the end of 2025?",
      category: "crypto",
      resolution_source: "https://coinmarketcap.com/",
      outcomes: ["Above $100,000", "$70,000 - $100,000", "$40,000 - $70,000", "Below $40,000"],
      min_stake: "0.01"
    },
    {
      title: "Ethereum 2.0 Staking Rewards",
      description: "What will Ethereum staking rewards average in 2025?",
      category: "crypto",
      resolution_source: "https://ethereum.org/",
      outcomes: ["Above 6%", "4-6%", "2-4%", "Below 2%"],
      min_stake: "0.01"
    }
  ],
  
  economics: [
    {
      title: "US GDP Growth 2025",
      description: "What will US GDP growth be in 2025 compared to 2024?",
      category: "economics",
      resolution_source: "https://www.bea.gov/",
      outcomes: ["Above 3%", "2-3%", "1-2%", "0-1%", "Negative Growth"],
      min_stake: "0.02"
    },
    {
      title: "Tesla Stock Performance 2025",
      description: "How will Tesla stock perform in 2025?",
      category: "economics",
      resolution_source: "https://finance.yahoo.com/",
      outcomes: ["Up >50%", "Up 20-50%", "Up 0-20%", "Down 0-20%", "Down >20%"],
      min_stake: "0.015"
    }
  ]
}

const quickCreateMarkets = [
  {
    title: "Bitcoin $100K in 2025?",
    description: "Will Bitcoin reach $100,000 by end of 2025?",
    category: "crypto",
    resolution_source: "https://coinmarketcap.com/",
    outcomes: ["Yes", "No"],
    min_stake: "0.01"
  },
  {
    title: "AI Breakthrough 2025",
    description: "Will there be a major AI breakthrough announcement in 2025?",
    category: "other",
    resolution_source: "https://techcrunch.com/",
    outcomes: ["Major Breakthrough", "Incremental Progress", "No Major News"],
    min_stake: "0.02"
  },
  {
    title: "Climate Target Met",
    description: "Will global emissions reduction targets be met this year?",
    category: "other",
    resolution_source: "https://unfccc.int/",
    outcomes: ["Targets Met", "Partially Met", "Targets Missed"],
    min_stake: "0.015"
  }
]

const formatCategory = (category) => {
  return category.charAt(0).toUpperCase() + category.slice(1)
}

const useTemplate = (market) => {
  emit('useTemplate', market)
}
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
