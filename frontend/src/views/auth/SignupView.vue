<template>
  <div class="min-h-screen flex items-center justify-center bg-linear-to-br from-[#e6f0fa] via-[#f4f8fb] to-[#c5def0]">
    <div class="md:w-full max-w-md rounded-lg border bg-white border-gray-300 shadow-md p-6">
      <div v-if="successmessage" class="text-green-500 text-center mb-4">{{ successmessage }}</div>
      <div v-if="errormessage" class="text-red-500 text-center mb-4">{{ errormessage }}</div>

      <form @submit.prevent="handleSubmit" class="max-w-md mx-auto  p-6" id="form">
        <h2 class="text-3xl font-bold text-center mb-6">
          Welcome to <span class="text-blue-600">UniAttend</span>
        </h2>

        <label for="name" class="block text-sm font-medium text-gray-700">Username</label>
        <input
          type="text"
          id="name"
          v-model="signupForm.username"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />

        <label for="email" class="block text-sm font-medium text-gray-700 mt-4">Email</label>
        <input
          type="email"
          id="email"
          v-model="signupForm.email"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />

        <label for="password" class="block text-sm font-medium text-gray-700 mt-4">Password</label>
        <input
          type="password"
          id="password"
          v-model="signupForm.password"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />

        <label for="phone" class="block text-sm font-medium text-gray-700 mt-4">Phone Number</label>
        <input
          type="tel"
          id="phone"
          v-model="signupForm.phonenumber"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        />

        <label for="role" class="block text-sm font-medium text-gray-700 mt-4">Role</label>
        <select
          id="role"
          v-model="signupForm.role"
          required
          class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
        >
          <option value="student">Student</option>
          <option value="organizer">Organizer</option>
        </select>

        <!-- Button with loading spinner -->
        <button
          type="submit"
          :disabled="loading"
          class="mt-6 w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-[#1a4c7a] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 flex items-center justify-center"
        >
          <span v-if="!loading">Register</span>
          <svg
            v-else
            class="animate-spin h-5 w-5 text-white"
            xmlns="http://www.w3.org/2000/svg"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              class="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              stroke-width="4"
            ></circle>
            <path
              class="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
            ></path>
          </svg>
        </button>

        <p class="mt-4 text-sm text-gray-600 text-center">
          Already have an account?
          <router-link :to="{ name: 'login' }" class="text-blue-600 hover:text-blue-800"
            >Log in</router-link
          >
        </p>
      </form>
    </div>
  </div>
</template>

<script>
import api from '../../axios';

export default {
  name: 'SignupView',
  data() {
    return {
      signupForm: {
        username: '',
        email: '',
        password: '',
        phonenumber: '',
        role: 'student',
      },
      errormessage: '',
      successmessage: '',
      loading: false, // New state for spinner
    };
  },
  methods: {
    async handleSubmit() {
      this.loading = true;
      this.errormessage = '';
      this.successmessage = '';

      try {
        const response = await api.post('/auth/register', this.signupForm);
        if (response.status === 201) {
          this.successmessage = response.data.message;
          setTimeout(() => {
            this.$router.push({ name: 'login' });
          }, 500);
        } else {
          this.errormessage = 'Signup failed: ' + response.data.message;
        }
      } catch (error) {
        this.errormessage = error.response
          ? error.response.data.message
          : 'An error occurred during signup. Please try again.';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
