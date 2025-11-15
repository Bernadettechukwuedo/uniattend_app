<!-- BackToTop.vue -->
<template>
  <button
    v-show="show"
    @click="scrollToTop"
    class="fixed bottom-6 right-6 bg-blue-600 text-white p-3 rounded-full w-[60px] shadow-md hover:bg-[#1a4c7a] transition duration-300"
  >
    ↑
  </button>
</template>

<script>
export default {
  data() {
    return {
      show: false,
    };
  },
  mounted() {
    window.addEventListener("scroll", this.handleScroll);
  },
  beforeUnmount() {
    window.removeEventListener("scroll", this.handleScroll);
  },
  methods: {
    handleScroll() {
      this.show = window.scrollY > 300;
    },
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: "smooth" });
    },
  },
};
</script>
