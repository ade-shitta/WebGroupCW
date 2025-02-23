// Example of how to use Vue Router

import { createRouter, createWebHistory } from 'vue-router'

// 1. Define route components.
// These can be imported from other files
import ProfilePage from '../pages/ProfilePage.vue';
import FriendsPage from '../pages/FriendsPage.vue';
import OtherUsersPage from '../pages/OtherUsersPage.vue';

let base = (import.meta.env.MODE == 'development') ? import.meta.env.BASE_URL : ''

// 2. Define some routes
// Each route should map to a component.
// We'll talk about nested routes later.
const router = createRouter({
    history: createWebHistory(base),
    routes: [
        { path: '/', name: 'Profile Page', component: ProfilePage },
        { path: '/friends/', name: 'Friends Page', component: FriendsPage },
        { path: '/otherusers/', name: 'Other Users Page', component: OtherUsersPage },
    ]
})

export default router
