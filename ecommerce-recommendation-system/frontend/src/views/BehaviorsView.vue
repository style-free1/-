<template>
  <el-card>
    <el-form :inline="true">
      <el-form-item label="用户ID"><el-input v-model="q.user_id" /></el-form-item>
      <el-form-item label="商品ID"><el-input v-model="q.product_id" /></el-form-item>
      <el-form-item label="行为类型"><el-select v-model="q.behavior_type" clearable style="width:130px;"><el-option label="view" value="view"/><el-option label="favorite" value="favorite"/><el-option label="cart" value="cart"/><el-option label="buy" value="buy"/><el-option label="review" value="review"/></el-select></el-form-item>
      <el-button type="primary" @click="load">筛选</el-button>
    </el-form>
    <el-table :data="list">
      <el-table-column prop="id" label="ID" width="70"/>
      <el-table-column prop="user_id" label="用户"/>
      <el-table-column prop="product_id" label="商品"/>
      <el-table-column prop="behavior_type" label="行为"/>
      <el-table-column prop="score" label="分值"/>
      <el-table-column prop="created_at" label="时间"/>
    </el-table>
  </el-card>
</template>
<script setup>
import { reactive, ref, onMounted } from 'vue'
import http from '../api/http'
const q = reactive({ user_id: '', product_id: '', behavior_type: '' })
const list = ref([])
const load = async () => { list.value = (await http.get('/api/behaviors', { params: q })).data }
onMounted(load)
</script>
