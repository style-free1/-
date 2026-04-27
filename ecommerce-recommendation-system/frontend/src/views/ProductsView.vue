<template>
  <el-card>
    <el-button type="primary" @click="load">刷新商品</el-button>
    <el-table :data="list" style="margin-top:10px;">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="name" label="商品名称" />
      <el-table-column prop="category" label="分类" />
      <el-table-column prop="price" label="价格" />
      <el-table-column prop="sales" label="销量" />
      <el-table-column prop="rating" label="评分" />
    </el-table>
  </el-card>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import http from '../api/http'
const list = ref([])
const load = async () => { list.value = (await http.get('/api/products')).data }
onMounted(load)
</script>
