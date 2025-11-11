<template>
  <footer class="bg-[#111827] text-white px-6 py-12">
    <div class="max-w-7xl mx-auto grid gap-10 md:grid-cols-3 items-start">
      
      <!-- Logo and Description -->
      <div >
        <img src="https://res.cloudinary.com/dotzzcayo/image/upload/v1762772780/MIXED_im8dd4.svg" alt="UniAttend Logo"  class="h-10 w-auto mb-4" />
        <p class="text-sm text-gray-300 mb-4">
          Making campus life more vibrant by helping students explore events easily and giving organisers a simple way to connect with them.
        </p>
        <p class="text-xs text-gray-500">© 2025 UniAttend. All rights reserved.</p>
      </div>

      <!-- Navigation Links -->
      <div class="flex flex-col space-y-2">
        <h3 class="text-white font-semibold mb-2">Quick Links</h3>
        <router-link :to="{ name: 'home', hash: '#home' }" class="text-gray-300 hover:text-white text-sm">Home</router-link>
        <router-link :to="{ name: 'view-events' }" class="text-gray-300 hover:text-white text-sm">Events</router-link>
        <router-link :to="{ name: 'home', hash: '#about' }" class="text-gray-300 hover:text-white text-sm">About</router-link>
        <router-link to="/contact" class="text-gray-300 hover:text-white text-sm">Contact</router-link>
      </div>

      <!-- Policy Links -->
      <div class="flex flex-col space-y-2 mt-6 md:mt-0">
        <h3 class="text-white font-semibold mb-2">Legal</h3>
        <a href="#" class="text-gray-300 hover:text-white text-sm">Privacy Policy</a>
        <a href="#" class="text-gray-300 hover:text-white text-sm">Terms of Service</a>
        
      </div>

    </div>
  </footer>
</template>
