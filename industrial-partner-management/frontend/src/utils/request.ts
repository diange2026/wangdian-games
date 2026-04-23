import axios, { type AxiosInstance, type AxiosRequestConfig, type AxiosResponse, type InternalAxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'
import type { ApiResponse, ErrorResponse } from '@/types/personnel'

// 创建axios实例
const service: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
service.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 在发送请求之前做些什么
    // 可以在这里添加token等认证信息
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    
    // 如果是FormData，删除Content-Type，让浏览器自动设置
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }
    
    return config
  },
  (error: any) => {
    // 对请求错误做些什么
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  (response: AxiosResponse) => {
    // 对响应数据做点什么
    const res = response.data
    
    // 如果后端有自定义的错误码，可以在这里处理
    if (res.code && res.code !== 0) {
      ElMessage.error(res.message || '请求失败')
      return Promise.reject(new Error(res.message || 'Error'))
    }
    
    // 直接返回数据
    return res
  },
  (error: any) => {
    // 对响应错误做点什么
    console.error('Response error:', error)
    
    let errorMessage = '请求失败'
    
    if (error.response) {
      // 服务器返回的错误
      const status = error.response.status
      const data = error.response.data as ErrorResponse
      
      switch (status) {
        case 400:
          errorMessage = data.detail || '请求参数错误'
          break
        case 401:
          errorMessage = '未授权，请重新登录'
          // 可以在这里跳转到登录页面
          localStorage.removeItem('access_token')
          window.location.href = '/login'
          break
        case 403:
          errorMessage = '拒绝访问'
          break
        case 404:
          errorMessage = '请求的资源不存在'
          break
        case 500:
          errorMessage = '服务器内部错误'
          break
        case 502:
          errorMessage = '网关错误'
          break
        case 503:
          errorMessage = '服务不可用'
          break
        case 504:
          errorMessage = '网关超时'
          break
        default:
          errorMessage = data.detail || `请求失败 (${status})`
      }
    } else if (error.request) {
      // 请求已发出，但没有收到响应
      errorMessage = '网络连接失败，请检查网络设置'
    } else {
      // 请求配置出错
      errorMessage = error.message || '请求配置错误'
    }
    
    // 显示错误消息
    ElMessage.error(errorMessage)
    
    return Promise.reject(error)
  }
)

// 封装请求方法
const request = <T = any>(config: AxiosRequestConfig): Promise<T> => {
  return service.request(config)
}

// 导出常用的HTTP方法
export const get = <T = any>(url: string, params?: any, config?: AxiosRequestConfig): Promise<T> => {
  return request<T>({
    url,
    method: 'get',
    params,
    ...config
  })
}

export const post = <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
  return request<T>({
    url,
    method: 'post',
    data,
    ...config
  })
}

export const put = <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
  return request<T>({
    url,
    method: 'put',
    data,
    ...config
  })
}

export const del = <T = any>(url: string, params?: any, config?: AxiosRequestConfig): Promise<T> => {
  return request<T>({
    url,
    method: 'delete',
    params,
    ...config
  })
}

export const patch = <T = any>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
  return request<T>({
    url,
    method: 'patch',
    data,
    ...config
  })
}

export default request