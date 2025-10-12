// stores/auth.js
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    refresh_token: localStorage.getItem('refresh_token') || null,
    user: localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')) : null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    login({ token,refresh_token, user }) {
      this.token = token;
      this.refresh_token = refresh_token;
      this.user = user;
      localStorage.setItem('token', token);
      localStorage.setItem('refresh_token', refresh_token);
      localStorage.setItem('user', JSON.stringify(user));
    },
    logout() {
      this.token = null;
      this.user = null;
      this.refresh_token = null;
      localStorage.removeItem('token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
    },
    updateUser(updatedUser) {
    this.user = updatedUser;
    localStorage.setItem('user', JSON.stringify(updatedUser));
  }
  },
});
