<template>
  <div class="fixed inset-0 z-50 flex justify-center items-center bg-black/80">
    <!-- Loading Spinner Overlay -->
    <div
      v-if="loading"
      class="flex flex-col items-center justify-center bg-white p-8 rounded-lg shadow-md"
    >
      <svg
        class="animate-spin h-10 w-10 text-blue-600 mb-3"
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
      <p class="text-gray-700 font-medium">Loading registrations...</p>
    </div>

    <!-- Actual Content -->
    <div
      v-else
      class="relative max-w-md max-h-fit mx-4 p-6 bg-white rounded-lg shadow-lg"
    >
      <button
        @click="$emit('cancel')"
        class="absolute top-3 right-3 text-gray-500 hover:text-gray-700"
      >
        ✕
      </button>

      <div class="py-3 border-b">
        <h2 class="text-md font-bold text-gray-800">
          Registered Users - {{ eventId.name }}
        </h2>
        <p class="text-sm text-gray-400">
          Manage attendees and track check-in status for your event
        </p>
      </div>

      <div class="overflow-y-auto max-h-[65vh]">
        <table class="min-w-full text-left border-collapse">
          <thead class="bg-gray-100 text-gray-700 text-sm">
            <tr>
              <th class="p-4 font-medium">Name</th>
              <th class="p-4 font-medium">Email</th>
              <th class="p-4 font-medium">Registration Date</th>
              <th class="p-4 font-medium">Checked In</th>
            </tr>
          </thead>

          <tbody
            v-if="registrations.length"
            class="divide-y-2 divide-gray-200 text-sm"
          >
            <tr
              v-for="(reg, index) in registrations"
              :key="index"
              class="hover:bg-gray-50"
            >
              <td class="p-4">{{ reg.username }}</td>
              <td class="p-4">{{ reg.email }}</td>
              <td class="p-4">{{ reg.registration_date }}</td>
              <td class="p-4">
                <span
                  :class="reg.checked_in
                    ? 'text-green-600 font-medium'
                    : 'text-red-500 font-medium'"
                >
                  {{ reg.checked_in ? 'Yes' : 'No' }}
                </span>
              </td>
            </tr>
          </tbody>

          <tbody v-else class="text-center text-gray-500">
            <tr>
              <td colspan="4" class="p-4">No registrations found.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import api from "../axios";

export default {
  props: {
    eventId: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      registrations: [],
      loading: true, 
    };
  },
  mounted() {
    this.fetchRegistrations();
    document.body.classList.add("overflow-hidden");
  },
  unmounted() {
    document.body.classList.remove("overflow-hidden");
  },
  methods: {
    async fetchRegistrations() {
      try {
        const response = await api.get(
          "/registration/view-student-registrations",
          {
            params: {
              event_id: this.eventId.id,
            },
          }
        );
        this.registrations = response.data.registrations || [];
      } catch (error) {
        console.error(error.message);
      } finally {
        this.loading = false; 
      }
    },
  },
};
</script>
