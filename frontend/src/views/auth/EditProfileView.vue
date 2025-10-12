<template>
  <div>
  <div v-if="messagee" class="text-green-500 text-center mb-4">{{ messagee }}</div>
  <form @submit.prevent="handleSubmit" class="max-w-md mx-auto mt-10 mb-10 p-6 bg-white rounded-lg shadow-md" id="form">
    <div v-if="errormessage" class="text-red-500 text-center mb-4">{{ errormessage }}</div>

    <h2 class="text-3xl font-bold text-center mb-6">Edit Profile</h2>

    <label for="name" class="block text-sm font-medium text-gray-700">Username</label>
    <input
      type="text"
      id="name"
      name="name"
      required
      v-model="editForm.username"
      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
    />

    <label for="email" class="block text-sm font-medium text-gray-700 mt-4">Email</label>
    <input
      type="email"
      v-model="editForm.email"
      id="email"
      name="email"
      required
      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
    />

    <label for="phone" class="block text-sm font-medium text-gray-700 mt-4">Phone Number</label>
    <input
      type="tel"
      v-model="editForm.phonenumber"
      id="phone"
      name="phone"
      required
      class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
    />

    <button
      class="mt-6 w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-[#1a4c7a] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
    >
      Save
    </button>
  </form></div>
</template>

<script>
import api from '../../axios';
import { useAuthStore } from '../../stores/auth.js';
import { storeToRefs } from 'pinia';

export default {
  name: 'EditProfileView',
  data() {
    const authStore = useAuthStore();
    const { user } = storeToRefs(authStore);
    return {
      authStore,
      user,
      editForm: {
        username: user.value.username,
        email: user.value.email,
        phonenumber: user.value.phonenumber,
        id: user.value.id, 
      },
      errormessage: '',
      messagee: '',
    };
  },
    mounted() {
    const authStore = useAuthStore();
    const { isAuthenticated } = storeToRefs(authStore);

    if (!isAuthenticated.value) {
        this.$router.push({ name: 'login' });
    }
    },
  methods: {
    async handleSubmit() {
      try {
        const response = await api.patch(`${import.meta.env.VITE_API_BASE_URL}/auth/update-user`, this.editForm);
        if (response.status === 200) {
          this.messagee = 'Profile updated successfully!';
          this.errormessage = '';
          this.authStore.updateUser(response.data.user); 
            if(response.data.user.role === 'student') {
                this.$router.push({ name: 'student-dashboard' });
                
            }
            else if(response.data.user.role === 'organizer') {
                this.$router.push({ name: 'organizer-dashboard' });

            }
            else if(response.data.user.role === 'admin') {
                this.$router.push({ name: 'admin-dashboard' });

            }
        } else {
          this.errormessage = 'Update failed: ' + response.data.detail;
        }
      } catch (error) {
        this.errormessage = error.response?.data?.detail || 'An error occurred while updating the profile.';
      }
    },
  },
};
</script>
