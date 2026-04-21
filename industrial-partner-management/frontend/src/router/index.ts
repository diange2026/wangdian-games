import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import Layout from '../layouts/BasicLayout.vue'
import { useAuthStore } from '../store/auth'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/auth/Login.vue'),
    meta: {
      title: '登录',
      requiresAuth: false
    }
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    meta: {
      requiresAuth: true
    },
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('../views/dashboard/index.vue'),
        meta: {
          title: '仪表板',
          icon: 'House',
          requiresAuth: true
        }
      },
      {
        path: 'companies',
        name: 'Companies',
        redirect: '/companies/list',
        meta: {
          title: '单位管理',
          icon: 'OfficeBuilding',
          requiresAuth: true
        },
        children: [
          {
            path: 'list',
            name: 'CompanyList',
            component: () => import('../views/companies/List.vue'),
            meta: {
              title: '单位列表',
              requiresAuth: true
            }
          },
          {
            path: 'create',
            name: 'CompanyCreate',
            component: () => import('../views/companies/Create.vue'),
            meta: {
              title: '创建单位',
              requiresAuth: true
            }
          },
          {
            path: 'edit/:id',
            name: 'CompanyEdit',
            component: () => import('../views/companies/Edit.vue'),
            meta: {
              title: '编辑单位',
              requiresAuth: true,
              hidden: true
            }
          },
          {
            path: 'detail/:id',
            name: 'CompanyDetail',
            component: () => import('../views/companies/Detail.vue'),
            meta: {
              title: '单位详情',
              requiresAuth: true,
              hidden: true
            }
          }
        ]
      },
      {
        path: 'certificates',
        name: 'Certificates',
        redirect: '/certificates/list',
        meta: {
          title: '证照管理',
          icon: 'Document',
          requiresAuth: true
        },
        children: [
          {
            path: 'list',
            name: 'CertificateList',
            component: () => import('../views/certificates/List.vue'),
            meta: {
              title: '证照列表',
              requiresAuth: true
            }
          }
        ]
      },
      {
        path: 'alerts',
        name: 'Alerts',
        component: () => import('../views/alerts/index.vue'),
        meta: {
          title: '预警管理',
          icon: 'Bell',
          requiresAuth: true
        }
      },
      {
        path: 'reports',
        name: 'Reports',
        component: () => import('../views/reports/index.vue'),
        meta: {
          title: '统计分析',
          icon: 'PieChart',
          requiresAuth: true
        }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('../views/settings/index.vue'),
        meta: {
          title: '系统设置',
          icon: 'Setting',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/error/404.vue'),
    meta: {
      title: '页面不存在',
      requiresAuth: false
    }
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 路由守卫
router.beforeEach(async (to, from, next) => {
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - ${import.meta.env.VITE_APP_TITLE}`
  }

  const authStore = useAuthStore()
  
  // 检查是否需要认证
  if (to.meta.requiresAuth) {
    // 检查token是否有效
    if (authStore.isAuthenticated) {
      next()
    } else {
      // 跳转到登录页
      next({
        path: '/login',
        query: { redirect: to.fullPath }
      })
    }
  } else {
    next()
  }
})

export default router