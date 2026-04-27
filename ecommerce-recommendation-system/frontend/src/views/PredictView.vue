<template>
  <el-card>
    <el-form :inline="true">
      <el-form-item label="用户ID"><el-input v-model.number="form.user_id" /></el-form-item>
      <el-form-item label="商品ID"><el-input v-model.number="form.product_id" /></el-form-item>
      <el-button type="primary" @click="run">预测</el-button>
    </el-form>
    <el-descriptions v-if="res" :column="3" border>
      <el-descriptions-item label="点击概率">{{ res.click_prob }}</el-descriptions-item>
      <el-descriptions-item label="加购概率">{{ res.cart_prob }}</el-descriptions-item>
      <el-descriptions-item label="购买概率">{{ res.buy_prob }}</el-descriptions-item>
    </el-descriptions>
  </el-card>
</template>
<script setup>
import { reactive, ref } from 'vue'
import http from '../api/http'
const form = reactive({ user_id: 1, product_id: 1 })
const res = ref(null)
const run = async () => { res.value = (await http.post('/api/predict', form)).data }
</script>
