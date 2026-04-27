<template>
  <el-container style="height:100vh;">
    <el-aside width="220px">
      <el-menu router default-active="/">
        <el-menu-item index="/">首页看板</el-menu-item>
        <el-menu-item index="/users">用户管理</el-menu-item>
        <el-menu-item index="/products">商品管理</el-menu-item>
        <el-menu-item index="/behaviors">行为数据</el-menu-item>
        <el-menu-item index="/predict">行为预测</el-menu-item>
        <el-menu-item index="/recommend">个性推荐</el-menu-item>
        <el-menu-item index="/system">系统管理</el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header style="display:flex;justify-content:space-between;align-items:center;">基于多源数据的电商用户行为预测与推荐系统 <el-button @click="logout">退出</el-button></el-header>
      <el-main><router-view /></el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
const router = useRouter()
const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>
