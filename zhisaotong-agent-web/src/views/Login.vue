<template>
   <div class="login-container">
      <div class="login-box">
         <h2>智扫通智能客服</h2>
         <el-form ref="loginFormRef" :model="loginForm" :rules="loginRules">
            <el-form-item prop="username">
               <el-input v-model="loginForm.username" placeholder="请输入用户名">
                  <template #prefix>
                     <User />
                  </template>
               </el-input>
            </el-form-item>
            <el-form-item prop="password">
               <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" show-password>
                  <template #prefix>
                     <Lock />
                  </template>
               </el-input>
            </el-form-item>
            <el-form-item>
               <el-button type="primary" class="login-btn" @click="handleLogin" :loading="loading">登 录</el-button>
            </el-form-item>
            <div class="link-box">
               <span class="link-text" @click="$router.push('/register')">立即注册</span>
            </div>
         </el-form>
      </div>
   </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { loginApi } from '@/api/user'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const loginFormRef = ref(null)
const loading = ref(false)
const loginForm = reactive({ username: '', password: '' })
const loginRules = {
   username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
   password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}


const userStore = useUserStore()

const handleLogin = async () => {
   const valid = await loginFormRef.value.validate()
   if (!valid) return

   loading.value = true
   try {
      const res = await loginApi(loginForm)

      const token = res.data.token
      const userInfo = res.data.user_info

      userStore.setToken(token)
      userStore.setUserInfo(userInfo)

      ElMessage.success('登录成功')
      router.push('/chat')
   } catch (err) {
      ElMessage.error('登录失败：' + (err.message || '网络异常'))
   } finally {
      loading.value = false
   }
}
</script>

<style scoped>
.login-container {
   width: 100%;
   height: 100%;
   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
   display: flex;
   align-items: center;
   justify-content: center;
   padding: 20px;
}

.login-box {
   width: 100%;
   max-width: 420px;
   padding: 32px 24px;
   background: #fff;
   border-radius: 16px;
   box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

h2 {
   text-align: center;
   margin-bottom: 24px;
   font-size: 22px;
}

.login-btn {
   width: 100%;
   height: 44px;
}

.link-box {
   text-align: right;
   margin-top: 8px;
}

.link-text {
   color: #409eff;
   cursor: pointer;
   font-size: 14px;
}
</style>