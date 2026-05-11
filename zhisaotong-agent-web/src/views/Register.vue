<template>
   <div class="register-container">
      <div class="register-box">
         <h2>账号注册</h2>
         <el-form ref="regFormRef" :model="regForm" :rules="regRules">
            <el-form-item prop="username">
               <el-input v-model="regForm.username" placeholder="用户名">
                  <template #prefix>
                     <User />
                  </template>
               </el-input>
            </el-form-item>
            <el-form-item prop="phone">
               <el-input v-model="regForm.phone" placeholder="手机号">
                  <template #prefix>
                     <Phone />
                  </template>
               </el-input>
            </el-form-item>
            <el-form-item prop="password">
               <el-input v-model="regForm.password" type="password" placeholder="密码" show-password>
                  <template #prefix>
                     <Lock />
                  </template>
               </el-input>
            </el-form-item>
            <el-form-item prop="confirmPassword">
               <el-input v-model="regForm.confirmPassword" type="password" placeholder="确认密码" show-password>
                  <template #prefix>
                     <Lock />
                  </template>
               </el-input>
            </el-form-item>
            <el-form-item>
               <el-button type="primary" class="reg-btn" @click="handleRegister" :loading="loading">注 册</el-button>
            </el-form-item>
            <div class="link-wrap">
               <span class="link-text" @click="$router.push('/login')">已有账号？立即登录</span>
            </div>
         </el-form>
      </div>
   </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Phone, Lock } from '@element-plus/icons-vue'
import { registerApi } from '@/api/user'
import { useUserStore } from '@/stores/user'

const router = useRouter()
const regFormRef = ref(null)
const loading = ref(false)
const regForm = reactive({ username: '', phone: '', password: '', confirmPassword: '' })

// 创建 store 实例
const userStore = useUserStore()

const regRules = {
   username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
   phone: [
      { required: true, message: '请输入手机号', trigger: 'blur' },
      { pattern: /^1[3-9]\d{9}$/, message: '手机号格式不正确', trigger: 'blur' }
   ],
   password: [
      { required: true, message: '请输入密码', trigger: 'blur' },
      { min: 6, message: '至少6位', trigger: 'blur' }
   ],
   confirmPassword: [
      { required: true, message: '请确认密码', trigger: 'blur' },
      {
         validator: (rule, value, callback) => {
            if (value !== regForm.password) callback(new Error('两次输入密码不一致'))
            else callback()
         }, trigger: 'blur'
      }
   ]
}

const handleRegister = async () => {
   const valid = await regFormRef.value.validate()
   if (!valid) return

   loading.value = true
   try {
      const res = await registerApi(regForm)

      // 1. 存储带 Bearer 的 token
      const token = 'Bearer ' + res.data.token
      localStorage.setItem('token', token)

      // 2. 存用户信息
      userStore.setUserInfo(res.data.user_info)

      ElMessage.success('注册成功')

      // 3. 延迟跳，让 localStorage 写入完成
      setTimeout(() => {
         router.push('/chat')
      }, 100)

   } catch (err) {
      ElMessage.error('注册失败：' + (err.message || '网络异常'))
   } finally {
      loading.value = false
   }
}
</script>

<style scoped>
.register-container {
   width: 100%;
   height: 100%;
   background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
   display: flex;
   align-items: center;
   justify-content: center;
   padding: 20px;
}

.register-box {
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

.reg-btn {
   width: 100%;
   height: 44px;
}

.link-wrap {
   text-align: right;
   margin-top: 8px;
}

.link-text {
   color: #409eff;
   cursor: pointer;
   font-size: 14px;
}
</style>