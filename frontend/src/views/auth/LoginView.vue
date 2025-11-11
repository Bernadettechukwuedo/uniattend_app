<template>
  <div class="min-h-screen flex items-center justify-center bg-linear-to-br from-[#e6f0fa] via-[#f4f8fb] to-[#c5def0]">
    <div class="md:w-full max-w-md bg-white rounded-lg border border-gray-300 shadow-md p-6">
    <div v-if="successmessage" class="text-green-500 text-center mb-4">{{ successmessage }}</div>

    <form @submit.prevent="handleSubmit" class="max-w-md mx-auto  mb-10 p-6  " id="form">
      <h2 class="text-3xl font-bold text-center mb-4">
        Sign In
      </h2>
      <p class="text-md text-gray-500 text-center mb-6">Enter your credentials to continue</p>

      <div v-if="errormessage" class="text-red-500 text-center mb-4">{{ errormessage }}</div>

      <label for="email" class="block text-sm font-medium text-gray-700">Email</label>
      <input type="email" id="email" name="email" required v-model="loginForm.email"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">

      <label for="password" class="block text-sm font-medium text-gray-700 mt-4">Password</label>
      <input type="password" v-model="loginForm.password" id="password" name="password" required
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm">


      <!-- Submit button with loading state -->
      <button type="submit"
        :disabled="loading"
        class="mt-6 w-full flex justify-center items-center bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-[#1a4c7a] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed">
        
        <span v-if="!loading">Login</span>
        <span v-else class="flex items-center gap-2">
          <svg class="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none"
            viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor"
              d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z">
            </path>
          </svg>
          Logging in...
        </span>
      </button>

      <p class="mt-4 text-sm text-gray-600 text-center">
        Don't have an account?
        <router-link :to="{ name: 'signup' }" class="text-blue-600 hover:text-blue-800">Sign Up</router-link>
      </p>
    </form>
  </div>
  </div>
</template>

<script>
import api from '../../axios';
import { useAuthStore } from '../../stores/auth.js';

export default {
  name: 'SignupView',
  data() {
    return {
      loginForm: {
        email: '',
        password: '',
      },
      password1: '',
      errormessage: '',
      successmessage: '',
      loading: false, // added loading state
    };
  },
  methods: {
    async handleSubmit() {


      this.loading = true; // start loading
      this.errormessage = '';
      this.successmessage = '';

      try {
        const response = await api.post('/auth/login', this.loginForm);
        if (response.status === 201) {
          this.successmessage = response.data.message;
          const auth = useAuthStore();
          auth.login({
            token: response.data.access_token,
            refresh_token: response.data.refresh_token,
            user: response.data.user
          });

          const role = response.data.user.role;
          if (role === 'student') this.$router.push({ name: 'student-dashboard' });
          else if (role === 'organizer') this.$router.push({ name: 'organizer-dashboard' });
          else if (role === 'admin') this.$router.push({ name: 'admin-dashboard' });
        } else {
          this.errormessage = "Login failed: " + response.data.message;
        }
      } catch (error) {
        if (error.response) {
          this.errormessage = error.response.data.message;
        } else {
          this.errormessage = "An error occurred during login. Please try again.";
        }
      } finally {
        this.loading = false; // stop loading
      }
    }
  }
};
</script>
