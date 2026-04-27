<template>
  <el-card>
    <el-button type="primary" @click="load">刷新用户</el-button>
    <el-table :data="list" style="margin-top:10px;">
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="email" label="邮箱" />
      <el-table-column prop="age" label="年龄" />
      <el-table-column prop="gender" label="性别" />
      <el-table-column prop="city" label="城市" />
    </el-table>
  </el-card>
</template>
<script setup>
import { ref, onMounted } from 'vue'
import http from '../api/http'
const list = ref([])
const load = async () => { list.value = (await http.get('/api/users')).data }
onMounted(load)
</script>
