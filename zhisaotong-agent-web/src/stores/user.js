import { defineStore } from 'pinia'
import request from '@/utils/request'

export const useUserStore = defineStore('user', {
   state: () => ({
      userInfo: {},
      token: localStorage.getItem('token') || ''
   }),

   actions: {
      setUserInfo(info) {
         this.userInfo = info
      },

      setToken(token) {
         this.token = token
         localStorage.setItem('token', token)
      },

      // 获取用户信息（页面加载用）
      async getUserInfo() {
         try {
            const res = await request.get('/user/info')
            this.userInfo = res.data
            return res.data
         } catch (err) {
            this.logout()
            throw err
         }
      },

      // 退出登录
      logout() {
         this.userInfo = {}
         this.token = ''
         localStorage.removeItem('token')

         // 跳回登录页
         window.location.href = '/login'
      }
   }
})