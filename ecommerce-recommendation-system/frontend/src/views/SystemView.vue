<template>
  <el-card>
    <h3>系统管理</h3>
    <el-space>
      <el-upload :auto-upload="false" :on-change="onFile"><el-button>选择CSV</el-button></el-upload>
      <el-select v-model="dataType" style="width:120px;"><el-option label="users" value="users"/><el-option label="products" value="products"/><el-option label="behaviors" value="behaviors"/></el-select>
      <el-button type="primary" @click="importData">数据导入</el-button>
      <el-button type="success" @click="train">模型训练</el-button>
      <el-button @click="refresh">推荐结果刷新</el-button>
    </el-space>
    <el-alert style="margin-top:12px;" :title="msg" type="info" :closable="false" />
  </el-card>
</template>
<script setup>
import { ref } from 'vue'
import http from '../api/http'
const msg = ref('待执行')
const dataType = ref('users')
const file = ref(null)
const onFile = (f) => { file.value = f.raw }
const importData = async () => {
  if (!file.value) return (msg.value = '请先选择CSV文件')
  const form = new FormData()
  form.append('file', file.value)
  const { data } = await http.post(`/api/model/import?data_type=${dataType.value}`, form)
  msg.value = JSON.stringify(data)
}
const train = async () => {
  const { data } = await http.post('/api/model/train')
  msg.value = '训练结果：' + JSON.stringify(data)
}
const refresh = () => {
  msg.value = '推荐缓存已刷新（演示版为实时计算）'
}
</script>
