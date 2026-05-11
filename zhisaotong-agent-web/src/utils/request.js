import axios from 'axios'

const request = axios.create({
   baseURL: '/api',
   timeout: 10000
})

// 请求拦截器
request.interceptors.request.use(config => {
   const token = localStorage.getItem('token')
   if (token) {
      config.headers.Authorization = token
   }
   return config
})

// 响应拦截器
request.interceptors.response.use(
   res => res.data,
   err => {
      const { response } = err
      if (response) {
         // 登录接口的 401 → 不跳转，只抛出错误
         if (response.status === 401 && response.config.url.includes('/user/login')) {
            return Promise.reject(response.data) // 交给页面提示
         }

         // 其他接口 401 → 才跳登录页
         if (response.status === 401) {
            localStorage.removeItem('token')
            location.href = '/login'
         }
      }
      return Promise.reject(err)
   }
)

export default request