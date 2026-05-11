import request from '@/utils/request'

// 用户登录
export function loginApi(data) {
   return request({
      url: '/user/login',
      method: 'post',
      data
   })
}

// 用户注册
export function registerApi(data) {
   return request({
      url: '/user/register',
      method: 'post',
      data
   })
}

// 获取用户信息
export function getUserInfoApi() {
   return request({
      url: '/user/info',
      method: 'get'
   })
}