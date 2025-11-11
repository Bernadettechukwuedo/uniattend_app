<template>
  <nav class="bg-gray-300 h-20 shadow-md flex items-center">
    <div class="flex items-center justify-between max-w-7xl mx-auto w-full px-4">
      
      <!-- Left: Logo -->
      <div class="flex items-center space-x-2">
        <img
          src="https://res.cloudinary.com/dotzzcayo/image/upload/v1762772780/MIXED_im8dd4.svg"
          alt="UniAttend logo"
          class="h-6 w-auto object-contain"
        />
      </div>

      <!-- Center: Main Nav Links -->
      <ul  v-if="!isAuthenticated" class="hidden md:flex space-x-6 absolute left-1/2 transform -translate-x-1/2">
        <li>
          <router-link :to="{name:'home', hash:'#home'}" class="text-black hover:text-[#1A4C7A] text-[16px] font-medium">Home</router-link>
        </li>
        <li>
          <router-link :to="{name:'view-events'}" class="text-black hover:text-[#1A4C7A] text-[16px] font-medium">Events</router-link>
        </li>
        <li>
          <router-link :to="{ name: 'home', hash: '#about' }" class="text-black hover:text-[#1A4C7A] text-[16px] font-medium">About</router-link>
        </li>
      </ul>

      <!-- Right: Auth Buttons -->
      <div class="flex space-x-4">
        <template v-if="isAuthenticated">
        <button @click.prevent="handleLogout" class=" text-white bg-red-600 p-3 rounded-md hover:bg-red-900">Logout</button>
      </template>
      <template v-else>
        <router-link :to="{name:'login'}" class=" bg-white px-4 py-2 rounded-md font-semibold hover:bg-[#1a4c7a] text-black hover:text-white">Login</router-link>
        <router-link :to="{name:'signup'}" class="text-white bg-blue-600 px-4 py-2 rounded-md hover:bg-[#1a4c7a] ">Sign Up</router-link>
      </template>
      </div>

    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth.js';
import { storeToRefs } from 'pinia';

const router = useRouter();
const authStore = useAuthStore();
const { user, isAuthenticated } = storeToRefs(authStore);

function handleLogout() {
  authStore.logout();
  router.push({ name: 'home' });
}
</script>
