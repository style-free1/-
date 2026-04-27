<template>
  <div style="height:100vh;display:flex;justify-content:center;align-items:center;background:#f2f6fc;">
    <el-card style="width:380px;">
      <h2>电商推荐系统登录</h2>
      <el-form>
        <el-form-item label="账号"><el-input v-model="form.username" /></el-form-item>
        <el-form-item label="密码"><el-input type="password" v-model="form.password" /></el-form-item>
        <el-button type="primary" @click="login" style="width:100%;">登录</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import http from '../api/http'

const router = useRouter()
const form = reactive({ username: 'admin', password: 'admin123' })

const login = async () => {
  try {
    const { data } = await http.post('/api/login', form)
    localStorage.setItem('token', data.access_token)
    ElMessage.success('登录成功')
    router.push('/')
  } catch (e) {
    ElMessage.error('登录失败')
  }
}
</script>
