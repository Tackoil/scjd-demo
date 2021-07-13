import { createRouter, createWebHistory } from 'vue-router'
import Display from './Display.vue'
import Manage from './Manage.vue'

export const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'display',
            component: Display,
        },
        {
            path: '/manage',
            name: 'manage',
            component: Manage,
        }
    ],
})