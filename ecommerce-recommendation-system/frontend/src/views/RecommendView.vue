<template>
  <el-card>
    <el-form :inline="true">
      <el-form-item label="用户ID"><el-input v-model.number="userId" /></el-form-item>
      <el-button type="primary" @click="run">获取推荐</el-button>
    </el-form>
    <el-table :data="items" style="margin-top:10px;">
      <el-table-column prop="product_id" label="商品ID" width="90"/>
      <el-table-column prop="product_name" label="商品名称"/>
      <el-table-column prop="score" label="推荐分"/>
      <el-table-column prop="reason" label="推荐理由"/>
    </el-table>
  </el-card>
</template>
<script setup>
import { ref } from 'vue'
import http from '../api/http'
const userId = ref(1)
const items = ref([])
const run = async () => { items.value = (await http.get(`/api/recommend/${userId.value}`)).data.items }
run()
</script>
