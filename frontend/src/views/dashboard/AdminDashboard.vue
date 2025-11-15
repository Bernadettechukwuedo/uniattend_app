<template>
  <div class="bg-linear-to-br from-[#e6f0fa] via-[#f4f8fb] to-[#c5def0]">
    <NavBar />
    <!-- Welcome Section -->
    <div class="bg-[#3D81B6]">
      <div class="max-w-7xl mx-auto px-4 sm:px-8 lg:px-8 py-4">
        <!-- Responsive layout -->
        <div
          class="flex flex-col md:flex-row justify-between items-center md:items-start mb-8 gap-6 mt-4"
        >
          <!-- Welcome text -->
          <div class="text-center md:text-left">
            <h1 class="text-2xl md:text-3xl font-bold text-white">
              Welcome, {{ user?.username }}!
            </h1>
            <p class="text-white mt-2">{{ user?.email }}</p>
          </div>

          <!-- Stats -->
          <div class="flex flex-wrap justify-center md:justify-end items-center gap-6">
            <div class="flex flex-col items-center">
              <h1 class="text-white font-bold text-xl">{{ countUsers }}</h1>
              <p class="text-white/60 text-sm">Total Users</p>
            </div>
            <div class="flex flex-col items-center">
              <h1 class="text-white font-bold text-xl">{{ countEvents }}</h1>
              <p class="text-white/60 text-sm">Total Events</p>
            </div>
            <div class="flex flex-col items-center">
              <h1 class="text-white font-bold text-xl">{{ countActive }}</h1>
              <p class="text-white/60 text-sm">Active Users</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Cards Section -->
    <div>
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <!-- Total Users Card -->
          <div
            class="h-28 flex flex-col items-center justify-center bg-white border-[#E0E6ED] rounded-2xl shadow-sm hover:shadow-md transition-transform duration-300 transform hover:-translate-y-1 cursor-pointer"
          >
            <h2 class="font-semibold text-md md:text-xl text-[#1E6091]">Total Users</h2>
            <p class="text-2xl font-bold text-[#1E6091] mt-1">{{ countUsers }}</p>
          </div>

          <!-- Total Events Card -->
          <div
            class="h-28 flex flex-col items-center justify-center border bg-white border-[#E0E6ED] rounded-2xl shadow-sm hover:shadow-md transition-transform duration-300 transform hover:-translate-y-1 cursor-pointer"
          >
            <h2 class="font-semibold text-md md:text-xl text-[#1E6091]">Total Events</h2>
            <p class="text-2xl font-bold text-[#1E6091] mt-1">{{ countEvents }}</p>
          </div>

          <!-- Total Registrations Card -->
          <div
            class="h-28 flex flex-col items-center justify-center border bg-white border-[#E0E6ED] rounded-2xl shadow-sm hover:shadow-md transition-transform duration-300 transform hover:-translate-y-1 cursor-pointer"
          >
            <h2 class="font-semibold text-md md:text-xl text-[#1E6091]">Total Registrations</h2>
            <p class="text-2xl font-bold text-[#1E6091] mt-1">{{ countRegistration }}</p>
          </div>
        </div>
      </div>
    </div>

    <!--User management-->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="flex justify-between">
        <h1 class="text-xl font-semibold">User Management</h1>
        <div @click="toggleuser()">
          <button class="text-white p-2 rounded-md flex items-center gap-2 bg-[#2370AC] transition">
            <Icon icon="mdi:people" width="24" height="24" />

            <span class="text-sm">{{ views }}</span>
          </button>
        </div>
      </div>
    </div>
    <!--table-->
    <div v-if="!this.open" class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div class="border border-[#E9EBEF] p-6 rounded-xl bg-white shadow-md">
        <h1 class="font-semibold">All Users</h1>
        <p>Manage user accounts, view their details, and monitor their activity</p>
        <p
          v-if="errormessage"
          class="mt-3 px-3 py-2 rounded-md text-sm font-medium text-white bg-red-600"
        >
          {{ errormessage }}
        </p>

        <div class="overflow-y-auto max-h-[65vh] mt-4">
          <table class="min-w-full text-left border-collapse">
            <thead class="bg-gray-100 text-gray-700 text-sm">
              <tr>
                <th class="p-4 font-medium">User</th>
                <th class="p-4 font-medium">Role</th>
                <th class="p-4 font-medium">Contact</th>
                <th class="p-4 font-medium">Status</th>

                <th class="p-4 font-medium">Actions</th>
              </tr>
            </thead>
            <tbody v-if="users.length" class="divide-y-2 divide-gray-200 text-sm">
              <tr v-for="(user, index) in users" :key="index" class="hover:bg-gray-50">
                <td class="p-4">
                  <div class="flex flex-col">
                    <span class="font-medium text-gray-800">{{ user.username }}</span>
                    <span class="text-sm text-gray-500">{{ user.email }}</span>
                  </div>
                </td>
                <td class="p-4">{{ user.role }}</td>
                <td class="p-4">{{ user.phonenumber }}</td>
                <td class="p-3">
                  <span
                    :class="[
                      'px-1.5 py-0.5 rounded-md text-[10px] font-medium inline-block',
                      user.status === 'active'
                        ? 'bg-green-600 text-white'
                        : 'bg-red-600 text-white',
                    ]"
                  >
                    {{ user.status }}
                  </span>
                </td>

                <td class="p-4">
                  <div class="flex items-center space-x-2">
                    <button
                      @click="toggleAction(user.id, user.status)"
                      :class="[
                        'border border-gray-300 rounded-lg px-3 py-1.5 text-sm font-medium bg-white hover:bg-gray-100/60 transition',
                        user.status === 'active'
                          ? 'text-green-600 hover:text-black hover:bg-green-600'
                          : 'text-red-600 hover:text-black hover:bg-red-600',
                      ]"
                    >
                      {{ user.status }}
                    </button>

                    <button
                      @click="toggleEvent(user.id, user.role)"
                      class="border border-gray-300 rounded-lg px-3 py-1.5 text-sm text-white font-medium bg-[#2370AC] hover:bg-[#023e6f] transition"
                    >
                      events
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
            <tbody v-else class="text-center text-gray-500">
              <tr>
                <td colspan="5" class="p-4">No user found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <!-- User Events Modal (Popup with Blur) -->
    <transition name="fade">
      <div
        v-if="show"
        class="fixed inset-0 flex items-center justify-center bg-black/40 backdrop-blur-sm z-50"
      >
        <div class="bg-white w-full max-w-lg rounded-xl shadow-xl p-6 relative animate-fadeIn">
          <!-- Close Button -->
          <button
            @click="show = false"
            class="absolute top-3 right-3 text-gray-500 hover:text-gray-700 text-xl font-bold"
          >
            <Icon icon="mdi:cancel-bold" width="24" height="24" />
          </button>

          <!-- Modal Header -->
          <div class="mb-4">
            <h1 class="font-semibold text-lg text-gray-800">User Events</h1>
            <p class="text-gray-500 text-sm">Events organized / registered by this user</p>
          </div>

        
          <!-- Loading Spinner Overlay -->
          <div
            v-if="loading"
            class="flex flex-col items-center justify-center "
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
            <p class="text-gray-700 font-medium">Loading events...</p>
          </div>
          <div v-else>
            <div v-if="user_events.length" class="space-y-3 max-h-[60vh] overflow-y-auto">
              <div
                v-for="(event, index) in user_events"
                :key="index"
                class="bg-white border border-gray-200 rounded-xl shadow-sm hover:shadow-md"
              >
                <img
                  :src="event.image"
                  alt="Sample Event"
                  class="w-full h-44 object-cover rounded-t-xl"
                />

                <!-- Event Content -->
                <div class="p-2">
                  <h2 class="text-lg font-semibold">{{ event.name }}</h2>
                  <p class="text-sm text-gray-600 mt-2 h-20">
                    {{ event.description }}
                  </p>

                  <!-- Date & Location -->
                  <p class="mt-4 text-sm text-gray-500 flex items-center gap-1">
                    <Icon
                      icon="material-symbols:calendar-clock-rounded"
                      width="24"
                      height="24"
                      class="text-blue-400"
                    />
                    {{ event.date }} at {{ event.time }}
                  </p>
                  <p class="mt-2 text-sm text-gray-500 flex items-center gap-1">
                    <Icon
                      icon="material-symbols:location-on"
                      width="24"
                      height="24"
                      class="text-red-400"
                    />
                    {{ event.location }}
                  </p>

                  <!-- Capacity & Organizer -->
                  <div class="flex justify-between mt-3">
                    <p class="text-sm text-gray-600 flex items-center gap-1">
                      <Icon
                        icon="mdi:account-group-outline"
                        width="20"
                        height="20 "
                        class="text-blue-400"
                      />Available Slots:
                      {{ event.capacity }}
                    </p>
                    <p class="text-sm text-gray-600">
                      by <span class="capitalize">{{ event.organizer }}</span>
                    </p>
                  </div>
                </div>
              </div>
            </div>
            <div v-else class="text-gray-500 text-center py-6">No events found for this user.</div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Admin Actions -->
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <h3 class="text-lg font-medium text-gray-700 mb-6">Admin Actions</h3>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <!-- User Analytics -->
        <div
          class="flex flex-col items-center justify-center border border-gray-100 p-5 rounded-lg bg-gray-50 shadow-sm hover:bg-gray-100/60 transition-colors duration-300"
        >
          <Icon icon="mdi:analytics" width="40" height="40" class="text-[#2370AC]" />
          <h2 class="text-gray-600 text-base font-normal mt-2">User Analytics</h2>
        </div>

        <!-- Event Reports -->
        <div
          class="flex flex-col items-center justify-center border border-gray-100 p-5 rounded-lg bg-gray-50 shadow-sm hover:bg-gray-100/60 transition-colors duration-300"
        >
          <Icon
            icon="material-symbols:analytics-outline-rounded"
            width="40"
            height="40"
            class="text-[#2370AC]"
          />
          <h2 class="text-gray-600 text-base font-normal mt-2">Event Reports</h2>
        </div>
      </div>
    </div>

    <Footer />
  </div>
</template>

<script>
import NavBar from '../../components/NavBar.vue';
import Footer from '../../components/Footer.vue';
import { useAuthStore } from '../../stores/auth.js';
import { storeToRefs } from 'pinia';
import api from '../../axios';
import { Icon } from '@iconify/vue';

export default {
  name: 'admin-dashboard',
  components: {
    NavBar,
    Footer,
    Icon,
  },
  data() {
    return {
      user: null,
      open: false,
      views: 'View All Users',
      users: [],
      countUsers: 0,
      countEvents: 0,
      countActive: 0,
      countRegistration: 0,
      userStatus: '',
      user_events: [],
      show: false,
      errormessage: '',
      loading: true,
    };
  },
  async mounted() {
    const authStore = useAuthStore();
    const { isAuthenticated, user } = storeToRefs(authStore);

    if (!isAuthenticated.value) {
      this.$router.push({ name: 'login' });
    } else {
      this.user = user.value;
      await this.fetchDetails();
    }
  },
  methods: {
    toggleuser() {
      this.open = !this.open;
      this.views = this.open ? 'View All Users' : 'Hide All Users';
    },
    async fetchDetails() {
      try {
        const user_response = await api.get('/auth/get-users');
        this.users = user_response.data;
        this.countUsers = this.users.length;

        const activeUser = this.users.filter((user) => user.status === 'active');
        this.countActive = activeUser.length;

        const event_response = await api.get('/events/get-events');
        this.countEvents = event_response.data.total;

        const registration_response = await api.get('/registration/get-registration');
        this.registrations = registration_response.data;
        this.countRegistration = this.registrations.length;
      } catch (error) {
        console.error('Error fetching user details:', error);
      }
      finally{
        this.loading = false;
      }
    },
    async toggleAction(id, userStatus) {
      try {
        const newStatus = userStatus === 'active' ? 'banned' : 'active';

        await api.patch('/auth/toggle-status', {
          id,
          status: newStatus,
        });
        const user = this.users.find((u) => u.id === id);
        if (user) user.status = newStatus;
        this.countActive = this.users.filter((u) => u.status === 'active').length;
      } catch (error) {
        // Safely extract backend error message
        if (error.response && error.response.data) {
          this.errormessage = error.response.data.detail || 'An unexpected error occurred.';
        } else {
          this.errormessage = 'Network error or server not reachable.';
        }

        //console.error("Toggle Status Error:", error);

        setTimeout(() => {
          this.errormessage = '';
        }, 5000);
      }
    },
    async toggleEvent(id, role) {
      try {
        this.loading = true;
        this.show = true;
        if (role === 'organizer') {
          const response_data = await api.get(`/events/organizer-event/${id}`);
          this.user_events = response_data.data.events;
        } else if (role === 'student') {
          const response_data = await api.get(`/registration/get-registrations/${id}`);
          this.user_events = response_data.data.registrations;
        } else {
          this.user_events = [];
        }
      } catch (error) {
        console.error('Error toggling event status:', error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>
<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

@keyframes fadeIn {
  from {
    transform: translateY(10px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}
.animate-fadeIn {
  animation: fadeIn 0.3s ease;
}
</style>
