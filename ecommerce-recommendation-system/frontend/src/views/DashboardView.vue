<template>
  <el-row :gutter="12">
    <el-col :span="6" v-for="c in cards" :key="c.label"><el-card><h4>{{ c.label }}</h4><h2>{{ c.value }}</h2></el-card></el-col>
  </el-row>
  <el-row :gutter="12" style="margin-top:12px;">
    <el-col :span="12"><el-card><div ref="pieRef" style="height:320px;" /></el-card></el-col>
    <el-col :span="12"><el-card><div ref="lineRef" style="height:320px;" /></el-card></el-col>
  </el-row>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import http from '../api/http'

const cards = ref([
  { label: '用户数量', value: 0 },
  { label: '商品数量', value: 0 },
  { label: '行为日志数量', value: 0 },
  { label: '推荐点击率', value: 0 }
])
const pieRef = ref()
const lineRef = ref()

onMounted(async () => {
  const { data } = await http.get('/api/dashboard/stats')
  cards.value[0].value = data.user_count
  cards.value[1].value = data.product_count
  cards.value[2].value = data.behavior_count
  cards.value[3].value = (data.recommend_ctr * 100).toFixed(2) + '%'

  echarts.init(pieRef.value).setOption({
    title: { text: '行为类型分布' },
    tooltip: {},
    series: [{ type: 'pie', data: Object.entries(data.behavior_distribution).map(([name, value]) => ({ name, value })) }]
  })
  echarts.init(lineRef.value).setOption({
    title: { text: '推荐效果折线图' },
    xAxis: { type: 'category', data: data.recommend_trend.map(i => i.date) },
    yAxis: { type: 'value' },
    series: [{ type: 'line', data: data.recommend_trend.map(i => i.ctr) }]
  })
})
</script>
