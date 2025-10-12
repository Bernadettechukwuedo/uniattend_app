import { createRouter, createWebHistory } from 'vue-router'
import LandingPage from '../views/LandingPage.vue'
import SignupView from '../views/auth/SignupView.vue'
import LoginView from '../views/auth/LoginView.vue'
import StudentDashboard from '../views/dashboard/StudentDashboard.vue'
import OrganizerDashboard from '../views/dashboard/OrganizerDashboard.vue'
import AdminDashboard from '../views/dashboard/AdminDashboard.vue'
import EventPage from '../views/EventPage.vue'
import NotFound from '../components/NotFound.vue'
import EditProfileView from '../views/auth/EditProfileView.vue'
import CreateEventForm from '../views/CreateEventForm.vue'
import { useAuthStore } from '../stores/auth';

const routes = [
  { path: '/', name: 'home', component: LandingPage },
  { path: '/signup', name: 'signup', component: SignupView },
  { path: '/login', name: 'login', component: LoginView },
  {
    path: '/student-dashboard',
    name: 'student-dashboard',
    component: StudentDashboard,
    meta: { requiresAuth: true },
  },
  {
    path: '/organizer-dashboard',
    name: 'organizer-dashboard',
    component: OrganizerDashboard,
    meta: { requiresAuth: true },
  },
  {
    path: '/admin-dashboard',
    name: 'admin-dashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true },
  },
  {
    path: '/events',
    name: 'view-events',
    component: EventPage,
  },
  {
    path: '/edit-profile',
    name: 'edit-profile',
    component: EditProfileView,
    meta: { requiresAuth: true }

  },
  {
    path: '/create-event',
    name: 'create-event',
    component: CreateEventForm,
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
  }

]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth',
      };
    }
    return { top: 0 };
  },
})
router.beforeEach((to, from, next) => {
  const auth = useAuthStore();

  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router