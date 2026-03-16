<template>
  <div id="app">
    <!-- 导航栏 -->
    <el-container>
      <el-header style="background-color: #409EFF; color: white; text-align: center; line-height: 60px;">
        <h1>货币基金套利提示系统</h1>
      </el-header>
      
      <el-container>
        <!-- 侧边栏导航 -->
        <el-aside width="200px" style="background-color: #f5f7fa; min-height: calc(100vh - 60px);">
          <el-menu
            :default-active="activeMenu"
            class="el-menu-vertical-demo"
            @select="handleMenuSelect"
            background-color="#f5f7fa"
            text-color="#333"
            active-text-color="#409EFF"
          >
            <el-menu-item index="overview">
              <el-icon><data-analysis /></el-icon>
              <span>综合数据</span>
            </el-menu-item>
            <el-menu-item index="funds">
              <el-icon><icon-menu /></el-icon>
              <span>基金列表</span>
            </el-menu-item>
            <el-menu-item index="prices">
              <el-icon><price-tag /></el-icon>
              <span>价格数据</span>
            </el-menu-item>
            <el-menu-item index="nav">
              <el-icon><trend-charts /></el-icon>
              <span>净值数据</span>
            </el-menu-item>
            <el-menu-item index="yields">
              <el-icon><data-analysis /></el-icon>
              <span>收益率数据</span>
            </el-menu-item>
            <el-menu-item index="alerts">
              <el-icon><bell /></el-icon>
              <span>提醒记录</span>
            </el-menu-item>
            <el-menu-item index="errors">
              <el-icon><warning /></el-icon>
              <span>错误记录</span>
            </el-menu-item>
          </el-menu>
        </el-aside>
        
        <!-- 主内容区域 -->
        <el-main style="padding: 20px;">
          <!-- 数据展示区域 -->
          <div class="data-container">
            <h2>{{ currentTitle }}</h2>
            
            <!-- 综合数据展示 -->
            <div v-if="activeMenu === 'overview'" class="data-section">
              <el-card>
                <template #header>
                  <div class="card-header">
                    <span>综合数据</span>
                    <el-button type="primary" @click="fetchOverview">刷新数据</el-button>
                  </div>
                </template>
                <el-table :data="overviewData" stripe style="width: 100%">
                  <el-table-column prop="fund_code" label="代码" width="120" />
                  <el-table-column prop="nav" label="净值" width="100" />
                  <el-table-column prop="buy_price" label="买入价" width="100" />
                  <el-table-column prop="yield_rate_buy" label="买入收益率" width="120" />
                  <el-table-column prop="sell_price" label="卖出价" width="100" />
                  <el-table-column prop="yield_rate_sell" label="卖出收益率" width="120" />
                </el-table>
              </el-card>
            </div>
            
            <!-- 基金列表展示 -->
            <div v-if="activeMenu === 'funds'" class="data-section">
              <el-card>
                <template #header>
                  <div class="card-header">
                    <span>基金列表</span>
                    <el-button type="primary" @click="fetchFunds">刷新数据</el-button>
                  </div>
                </template>
                <el-table :data="fundsData" stripe style="width: 100%">
                  <el-table-column prop="fund_code" label="基金代码" width="120" />
                  <el-table-column prop="fund_name" label="基金名称" />
                </el-table>
              </el-card>
            </div>
            
            <!-- 价格数据展示 -->
            <div v-if="activeMenu === 'prices'" class="data-section">
              <el-card>
                <template #header>
                  <div class="card-header">
                    <span>价格数据</span>
                    <el-button type="primary" @click="fetchPrices">刷新数据</el-button>
                  </div>
                </template>
                <el-table :data="pricesData" stripe style="width: 100%">
                  <el-table-column prop="fund_code" label="基金代码" width="120" />
                  <el-table-column prop="price" label="最新价" width="100" />
                  <el-table-column prop="buy_price" label="买入价" width="100" />
                  <el-table-column prop="sell_price" label="卖出价" width="100" />
                  <el-table-column prop="price_date" label="价格日期" width="150" />
                </el-table>
              </el-card>
            </div>
            
            <!-- 净值数据展示 -->
            <div v-if="activeMenu === 'nav'" class="data-section">
              <el-card>
                <template #header>
                  <div class="card-header">
                    <span>净值数据</span>
                    <el-button type="primary" @click="fetchNav">刷新数据</el-button>
                  </div>
                </template>
                <el-table :data="navData" stripe style="width: 100%">
                  <el-table-column prop="fund_code" label="基金代码" width="120" />
                  <el-table-column prop="nav" label="净值" width="120" />
                  <el-table-column prop="nav_date" label="净值日期" width="150" />
                </el-table>
              </el-card>
            </div>
            
            <!-- 收益率数据展示 -->
            <div v-if="activeMenu === 'yields'" class="data-section">
              <el-card>
                <template #header>
                  <div class="card-header">
                    <span>收益率数据</span>
                    <el-button type="primary" @click="fetchYields">刷新数据</el-button>
                  </div>
                </template>
                <el-table :data="yieldsData" stripe style="width: 100%">
                  <el-table-column prop="fund_code" label="基金代码" width="120" />
                  <el-table-column prop="yield_rate" label="收益率" width="120" />
                  <el-table-column prop="yield_rate_buy" label="买入收益率" width="120" />
                  <el-table-column prop="yield_rate_sell" label="卖出收益率" width="120" />
                  <el-table-column prop="yield_date" label="收益率日期" width="150" />
                </el-table>
              </el-card>
            </div>
            
            <!-- 提醒记录展示 -->
            <div v-if="activeMenu === 'alerts'" class="data-section">
              <el-card>
                <template #header>
                  <div class="card-header">
                    <span>提醒记录</span>
                    <el-button type="primary" @click="fetchAlerts">刷新数据</el-button>
                  </div>
                </template>
                <el-table :data="alertsData" stripe style="width: 100%">
                  <el-table-column prop="fund_code" label="基金代码" width="120" />
                  <el-table-column prop="fund_name" label="基金名称" />
                  <el-table-column prop="yield_rate" label="收益率" width="120" />
                  <el-table-column prop="created_at" label="创建时间" width="180" />
                </el-table>
              </el-card>
            </div>
            
            <!-- 错误记录展示 -->
            <div v-if="activeMenu === 'errors'" class="data-section">
              <el-card>
                <template #header>
                  <div class="card-header">
                    <span>错误记录</span>
                    <el-button type="primary" @click="fetchErrors">刷新数据</el-button>
                  </div>
                </template>
                <el-table :data="errorsData" stripe style="width: 100%">
                  <el-table-column prop="error_type" label="错误类型" width="150" />
                  <el-table-column prop="error_message" label="错误信息" />
                  <el-table-column prop="created_at" label="创建时间" width="180" />
                </el-table>
              </el-card>
            </div>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import {
  Menu as IconMenu,
  PriceTag,
  TrendCharts,
  DataAnalysis,
  Bell,
  Warning
} from '@element-plus/icons-vue'

// 响应式数据
const activeMenu = ref('overview')
const currentTitle = ref('综合数据')

const fundsData = ref([])
const pricesData = ref([])
const navData = ref([])
const yieldsData = ref([])
const alertsData = ref([])
const errorsData = ref([])
const overviewData = ref([])

// 菜单标题映射
const menuTitles = {
  overview: '综合数据',
  funds: '基金列表',
  prices: '价格数据',
  nav: '净值数据',
  yields: '收益率数据',
  alerts: '提醒记录',
  errors: '错误记录'
}

// 菜单选择处理
const handleMenuSelect = (index) => {
  activeMenu.value = index
  currentTitle.value = menuTitles[index]
  // 切换到对应菜单时自动加载数据
  switch (index) {
    case 'overview':
      fetchOverview()
      break
    case 'funds':
      fetchFunds()
      break
    case 'prices':
      fetchPrices()
      break
    case 'nav':
      fetchNav()
      break
    case 'yields':
      fetchYields()
      break
    case 'alerts':
      fetchAlerts()
      break
    case 'errors':
      fetchErrors()
      break
  }
}

// API调用函数
// 定义需要显示的基金代码
const selectedFunds = ['511880', '511990']

// 后端API基础URL
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:5001/api';

// 获取基金列表
const fetchFunds = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/funds`)
    const data = await response.json()
    if (data.data) {
      // 过滤只显示指定的基金
      fundsData.value = data.data.filter(fund => selectedFunds.includes(fund.fund_code))
    }
  } catch (error) {
    console.error('获取基金列表失败:', error)
    // 清空数据，不使用mock数据
    fundsData.value = []
  }
}

const fetchPrices = async () => {
  try {
    console.log('开始获取价格数据')
    console.log('API URL:', `${API_BASE_URL}/prices?limit=1000`)
    const response = await fetch(`${API_BASE_URL}/prices?limit=1000`)
    console.log('价格数据响应对象:', response)
    console.log('响应状态码:', response.status)
    console.log('响应状态文本:', response.statusText)
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}, statusText: ${response.statusText}`)
    }
    const data = await response.json()
    console.log('价格数据原始数据:', data)
    if (data.status === 'success' && data.data) {
      const filteredData = data.data.filter(item => selectedFunds.includes(String(item.fund_code)))
      console.log('价格数据过滤后数据:', filteredData)
      pricesData.value = filteredData
    } else {
      console.error('价格数据API返回错误:', data.message || '未知错误')
    }
  } catch (error) {
    console.error('获取价格数据失败:', error)
    console.error('错误类型:', typeof error)
    console.error('错误堆栈:', error.stack)
    pricesData.value = []
  }
}

const fetchNav = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/nav?limit=1000`)
    const data = await response.json()
    if (data.data) {
      // 过滤只显示指定的基金并按日期排序
      navData.value = data.data
        .filter(nav => selectedFunds.includes(nav.fund_code))
        .sort((a, b) => new Date(b.nav_date) - new Date(a.nav_date))
    }
  } catch (error) {
    console.error('获取净值数据失败:', error)
    // 清空数据，不使用mock数据
    navData.value = []
  }
}

const fetchYields = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/yields?limit=1000`)
    const data = await response.json()
    if (data.data) {
      // 过滤只显示指定的基金
      yieldsData.value = data.data.filter(yieldData => selectedFunds.includes(yieldData.fund_code))
    }
  } catch (error) {
    console.error('获取收益率数据失败:', error)
    // 清空数据，不使用mock数据
    yieldsData.value = []
  }
}

const fetchAlerts = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/alerts?limit=1000`)
    const data = await response.json()
    if (data.data) {
      // 过滤只显示指定的基金
      alertsData.value = data.data.filter(alert => selectedFunds.includes(alert.fund_code))
    }
  } catch (error) {
    console.error('获取提醒记录失败:', error)
  }
}

const fetchErrors = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/errors?limit=1000`)
    const data = await response.json()
    if (data.data) {
      errorsData.value = data.data
    }
  } catch (error) {
    console.error('获取错误记录失败:', error)
  }
}

// Mock数据
const mockFundData = [
  { fund_code: '511880', fund_name: '银华日利' },
  { fund_code: '511990', fund_name: '华宝添益' },
  { fund_code: '511800', fund_name: '易方达货币' },
  { fund_code: '511850', fund_name: '南方理财金H' }
];

const mockNavData = [
  { fund_code: '511880', nav: '100.02', nav_date: '2024-12-11' },
  { fund_code: '511990', nav: '100.01', nav_date: '2024-12-11' },
  { fund_code: '511800', nav: '100.00', nav_date: '2024-12-11' },
  { fund_code: '511850', nav: '100.03', nav_date: '2024-12-11' }
];

const mockPricesData = [
  { fund_code: '511880', buy_price: '100.01', sell_price: '100.03', price_date: '2024-12-11' },
  { fund_code: '511990', buy_price: '100.00', sell_price: '100.02', price_date: '2024-12-11' },
  { fund_code: '511800', buy_price: '99.99', sell_price: '100.01', price_date: '2024-12-11' },
  { fund_code: '511850', buy_price: '100.02', sell_price: '100.04', price_date: '2024-12-11' }
];

const mockYieldsData = [
  { fund_code: '511880', yield_rate_buy: '2.15', yield_rate_sell: '2.05', yield_date: '2024-12-11' },
  { fund_code: '511990', yield_rate_buy: '2.10', yield_rate_sell: '2.00', yield_date: '2024-12-11' },
  { fund_code: '511800', yield_rate_buy: '2.05', yield_rate_sell: '1.95', yield_date: '2024-12-11' },
  { fund_code: '511850', yield_rate_buy: '2.20', yield_rate_sell: '2.10', yield_date: '2024-12-11' }
];

// 获取综合数据
const fetchOverview = async () => {
  try {
    console.log('开始获取综合数据...')
    
    // 并行获取所有数据
    const [navResponse, pricesResponse, yieldsResponse, fundsResponse] = await Promise.all([
      fetch(`${API_BASE_URL}/nav?limit=1000`),
      fetch(`${API_BASE_URL}/prices?limit=1000`),
      fetch(`${API_BASE_URL}/yields?limit=1000`),
      fetch(`${API_BASE_URL}/funds`)
    ])
    
    // 解析响应数据
    const navData = await navResponse.json()
    const pricesData = await pricesResponse.json()
    const yieldsData = await yieldsResponse.json()
    const fundsData = await fundsResponse.json()
    
    // 过滤数据
    const filteredNav = navData.data ? navData.data.filter(nav => selectedFunds.includes(nav.fund_code)) : []
    const filteredPrices = pricesData.data ? pricesData.data.filter(price => selectedFunds.includes(price.fund_code)) : []
    const filteredYields = yieldsData.data ? yieldsData.data.filter(yieldData => selectedFunds.includes(yieldData.fund_code)) : []
    const fundList = fundsData.data ? fundsData.data : []
    
    // 整合数据
    const overview = []
    selectedFunds.forEach(fundCode => {
      // 找到最新的净值数据
      const nav = filteredNav
        .filter(n => n.fund_code === fundCode)
        .sort((a, b) => new Date(b.nav_date) - new Date(a.nav_date))[0]
      
      // 找到最新的价格数据
      const price = filteredPrices
        .filter(p => p.fund_code === fundCode)
        .sort((a, b) => new Date(b.price_date) - new Date(a.price_date))[0]
      
      // 找到最新的收益率数据
      const yieldData = filteredYields
        .filter(y => y.fund_code === fundCode)
        .sort((a, b) => new Date(b.yield_date) - new Date(a.yield_date))[0]
      
      // 找到基金名称
      const fund = fundList.find(f => f.fund_code === fundCode)
      
      if (nav && price && yieldData) {
        overview.push({
          fund_code: fundCode,
          fund_name: fund ? fund.fund_name : fundCode,
          nav: nav.nav,
          nav_date: nav.nav_date,
          buy_price: price.buy_price,
          sell_price: price.sell_price,
          price_date: price.price_date,
          yield_rate_buy: yieldData.yield_rate_buy,
          yield_rate_sell: yieldData.yield_rate_sell,
          yield_date: yieldData.yield_date
        })
      }
    })
    
    overviewData.value = overview
    console.log('综合数据更新成功:', overviewData.value)
  } catch (error) {
    console.error('获取综合数据失败:', error)
    // 清空数据，不使用mock数据
    overviewData.value = []
  }
}

// 组件挂载时加载初始数据
onMounted(() => {
  fetchOverview()
})
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  font-family: 'Helvetica Neue', Helvetica, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', '微软雅黑', Arial, sans-serif;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.data-section {
  margin-bottom: 20px;
}

.el-table {
  margin-top: 10px;
}

.el-header h1 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
}

.el-aside {
  border-right: 1px solid #e6e6e6;
}

.el-menu {
  border-right: none;
}

.el-menu-item {
  height: 56px;
  line-height: 56px;
}

.el-card {
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}
</style>
