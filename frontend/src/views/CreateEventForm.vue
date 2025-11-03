<template>
  <div>
    <div v-if="messagee" class="text-green-500 text-center mb-4">{{ messagee }}</div>
    <form @submit.prevent="handleSubmit" class="max-w-md mx-auto mt-10 mb-10 p-6 bg-white rounded-lg shadow-md" id="form" >
      <div v-if="errormessage" class="text-red-500 text-center mb-4">{{ errormessage }}</div>

      <h2 class="text-3xl font-bold text-center mb-6">Create Event</h2>

      <label for="name" class="block text-sm font-medium text-gray-700">Event name</label>
      <input
        type="text"
        id="name"
        name="name"
        required
        v-model="eventForm.name"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      />

      <label for="description" class="block text-sm font-medium text-gray-700 mt-4">Description</label>
      <input
        type="text"
        v-model="eventForm.description"
        id="description"
        name="description"
        required
        placeholder="Write a short description of your event"
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      />

      <label for="date" class="block text-sm font-medium text-gray-700 mt-4">Date</label>
      <input
        type="date"
        v-model="eventForm.date"
        id="date"
        name="date"
        required
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      />

      <label for="time" class="block text-sm font-medium text-gray-700 mt-4">Time</label>
      <input
        type="time"
        v-model="eventForm.time"
        id="time"
        name="time"
        required
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      />

      <label for="location" class="block text-sm font-medium text-gray-700 mt-4">Location</label>
      <input
        type="tel"
        v-model="eventForm.location"
        id="location"
        name="location"
        required
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      />
      <label for="capacity" class="block text-sm font-medium text-gray-700 mt-4">Capacity</label>
      <input
        type="number"
        v-model="eventForm.capacity"
        id="capacity"
        name="capacity"
        required
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      />

      <label for="organiser" class="block text-sm font-medium text-gray-700 mt-4">Organiser</label>
      <input
        type="text"
        v-model="eventForm.organizer"
        id="organiser"
        name="organiser"
        required
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      />

      <label for="image" class="block text-sm font-medium text-gray-700 mt-4">Image</label>
      <input
        type="file"
        @change="handleFileChange"
        id="image"
        name="image"
        required
        class="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
      />

      <button
        class="mt-6 w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-[#1a4c7a] focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      >
        Save
      </button>
    </form>
  </div>
</template>

<script>
import api from '../axios';
import { useAuthStore } from '../stores/auth.js';
import { storeToRefs } from 'pinia';

export default {
  name: 'CreateEventForm',
  data() {
    const authStore = useAuthStore();
    const { user } = storeToRefs(authStore);
    return {
      authStore,
      user,
      eventForm: {
        name: "",
        description: "",
        date: "",
        time: "",
        location: "",
        capacity: "",
        organizer: "",
        image: null,
        id: user.value?.id || null,
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

      handleFileChange(event) {
    this.eventForm.image = event.target.files[0];
  },
    async handleSubmit() {
      try {
        this.messagee = '';
        this.errormessage = '';
        if(this.eventForm.capacity <= 0) {
          this.errormessage = 'Capacity must be greater than 0.';
          return;
        };
        const formData = new FormData();
        for(const key in this.eventForm) {
          formData.append(key, this.eventForm[key]);
        }
        const response = await api.post(`${import.meta.env.VITE_API_BASE_URL}/events/create-event`,formData,
        { headers: { "Content-Type": "multipart/form-data" } }
        );
        if (response.status === 201) {
          this.messagee = 'Event created successfully!';
          this.errormessage = '';

          setTimeout(() => {
            this.$router.push({ name: 'organizer-dashboard' });
            }, 1500);
        } else {
          this.errormessage = 'Event Creation failed: ' + response.data.detail;
        }
      } catch (error) {
        this.errormessage = error.response?.data?.detail || 'An error occurred while creating an event.';
      }
    },
  },
};
</script>
