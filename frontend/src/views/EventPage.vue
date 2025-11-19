<template>
  <div class="min-h-screen bg-white">
    <!-- Navbar -->
    <NavBar />

    <!-- Hero Image -->
    <div class="relative">
      <img
        src="https://res.cloudinary.com/dotzzcayo/image/upload/v1752767824/uni_gk8ii9.jpg"
        alt="Unn university library"
        class="w-full h-[500px] object-cover shadow-lg"
      />
      <div class="absolute inset-0 bg-linear-to-br from-[#1E5A8A] via-black/40 to-black"></div>
    </div>

    <!-- Event Overview Header -->
    <section class="px-4 md:px-16 py-8">
      <!-- Search Bar -->
      <div class="mb-8 max-w-xl mx-auto flex gap-4">
        <input
          v-model="searchQuery"
          @keyup.enter="fetchEvents"
          type="text"
          placeholder="Search for event title or description..."
          class="w-full p-3 rounded-xl border border-gray-300 focus:outline-none focus:ring-2 focus:ring-[#1E5A8A]"
          id="search"
        />
        <button
          @click="fetchEvents"
          class="bg-[#1E5A8A] text-white px-6 py-3 rounded-xl hover:bg-[#16456b]"
        >
          Search
        </button>
      </div>

      <!-- Events Grid or Loading Spinner -->
      <div>
        <div v-if="loading" class="flex justify-center items-center py-20">
          <svg
            class="animate-spin h-10 w-10 text-[#1E5A8A]"
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
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-8">
          <div
            v-for="event in filteredEvents"
            :key="event.id"
            class="bg-white border border-gray-200 rounded-xl shadow-md hover:shadow-lg transition transform hover:-translate-y-1 max-h-fit"
          >
            <img
              :src="event.image"
              alt="Event Image"
              class="w-full h-48 object-cover rounded-t-xl"
            />
            <div class="p-6">
              <h2 class="text-lg font-semibold">
                {{ event.name }}
              </h2>
              <p class="text-sm text-gray-600 h-25">
                {{ event.description }}
              </p>

              <p class="mt-6 text-sm text-gray-500 flex items-center gap-1">
                <Icon
                  icon="material-symbols:calendar-clock-rounded"
                  width="24"
                  height="24"
                  class="text-blue-400"
                />
                {{ event.date }} at {{ event.time }}
              </p>

              <p class="text-sm text-gray-600 flex items-center gap-1">
                <Icon
                  icon="mdi:account-group-outline"
                  width="20"
                  height="20"
                  class="text-blue-400"
                />
                Available Slots: {{ event.capacity }}
              </p>

              <div class="mt-6">
                <router-link
                  :to="{ name: 'signup' }"
                  class="bg-[#1E5A8A] text-white px-4 py-2 rounded-full hover:bg-[#16456b] transition"
                >
                  View more
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div
        class="mt-8 flex justify-center gap-4"
        v-if="filteredEvents.length > 0 && !loading"
      >
        <button
          @click="prevPage"
          :disabled="offset === 0"
          class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
        <button
          @click="nextPage"
          :disabled="filteredEvents.length < limit"
          class="px-4 py-2 bg-[#1E5A8A] text-white rounded hover:bg-[#16456b] disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
        </button>
      </div>

      <!-- No Results -->
      <div
        v-if="filteredEvents.length === 0 && !loading"
        class="text-center mt-12 text-gray-500"
      >
        No events found.
      </div>
    </section>

    <Footer />
  </div>
</template>

<script>
import NavBar from "../components/NavBar.vue";
import Footer from "../components/Footer.vue";
import api from "../axios";
import { Icon } from "@iconify/vue";

export default {
  name: "EventPage",
  components: {
    NavBar,
    Footer,
    Icon,
  },
  data() {
    return {
      searchQuery: "",
      events: [],
      limit: 3,
      offset: 0,
      total: 0,
      loading: false,
    };
  },
  methods: {
    async fetchEvents() {
      this.loading = true;
      try {
        const response = await api.get("/events/get-events", {
          params: {
            search: this.searchQuery,
            limit: this.limit,
            offset: this.offset,
          },
        });
        this.total = response.data.total;
        this.events = response.data.events.map((event) => ({
          ...event,
          image: event.image,
        }));
      } catch (error) {
        console.error("Error fetching events:", error);
        this.events = [];
      } finally {
        this.loading = false;
      }
    },
    nextPage() {
      if (this.limit + this.offset < this.total) {
        this.offset += this.limit;
        this.fetchEvents();
      }
    },
    prevPage() {
      if (this.offset > 0) {
        this.offset -= this.limit;
        this.fetchEvents();
      }
    },
  },
  mounted() {
    this.fetchEvents();
  },
  computed: {
    filteredEvents() {
      const today = new Date();
      today.setHours(0, 0, 0, 0);
      return this.events.filter((event) => {
        const eventDate = new Date(event.date);
        eventDate.setHours(0, 0, 0, 0);
        return eventDate >= today;
      });
    },
  },
};
</script>
