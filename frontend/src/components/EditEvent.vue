<template>
  <div class="fixed inset-0 z-50 flex justify-center items-center bg-black/80">
    <div class="relative max-w-md w-full mx-4 p-6 bg-white rounded-lg shadow-lg max-h-[90vh] overflow-y-auto" >
      <button
        @click="$emit('cancel')"
        class="absolute top-3 right-3 text-gray-500 hover:text-gray-700"
      >
        ✕
      </button>

      <h2 class="text-2xl font-bold text-center mb-6">Edit Event</h2>

      <div v-if="messagee" class="text-green-500 text-center mb-4">{{ messagee }}</div>
      <div v-if="errormessage" class="text-red-500 text-center mb-4">{{ errormessage }}</div>

      <!-- Form -->
      <form @submit.prevent="handleUpdate" class="space-y-4 ">
        <div>
        <label class="block" for="name">
          <span class="text-sm text-gray-700">Event name</span>
          <input
            type="text"
            v-model="event.name"
            required
            id="name"
            name="name"
             autocomplete="off"
            class="mt-1 block w-full border rounded-md px-3 py-2 shadow-sm"
          />
        </label>
        </div>

        <label class="block" for="description">
          <span class="text-sm text-gray-700">Description</span>
          <input
            type="text"
            v-model="event.description"
            required
            name="description"
            id="description"
             autocomplete="off"
            class="mt-1 block w-full border rounded-md px-3 py-2 shadow-sm"
          />
        </label>

        <label class="block" for="date">
          <span class="text-sm text-gray-700">Date</span>
          <input
            type="date"
            v-model="event.date"
            required
            id="date"
            name="date"
             autocomplete="off"
            class="mt-1 block w-full border rounded-md px-3 py-2 shadow-sm"
          />
        </label>

        <label class="block" for="time">
          <span class="text-sm text-gray-700">Time</span>
          <input
            type="time"
            id="time"
            name="time"
            v-model="event.time"
             autocomplete="off"
            required
            class="mt-1 block w-full border rounded-md px-3 py-2 shadow-sm"
          />
        </label>

        <label class="block" for="location">
          <span class="text-sm text-gray-700">Location</span>
          <input
            type="text"
            v-model="event.location"
            required
            id="location"
            name="location"
             autocomplete="off"
            class="mt-1 block w-full border rounded-md px-3 py-2 shadow-sm"
          />
        </label>

        <label class="block" for="capacity">
          <span class="text-sm text-gray-700">Existing Capacity</span>
          <input
            type="number"
            v-model.number="event.capacity"
            disabled
            id="capacity"
            name="capacity"
             autocomplete="off"
            class="mt-1 block w-full border rounded-md px-3 py-2 shadow-sm bg-gray-100"
          />
        </label>

        <label class="block" for="addextraseats">
          <span class="text-sm text-gray-700">Add extra seats</span>
          <input
            type="number"
            v-model.number="addextraseats"
            id="addextraseats"
            name="addextraseats"
             autocomplete="off"
             min="0"
             step="1"
            class="mt-1 block w-full border rounded-md px-3 py-2 shadow-sm"
          />
        </label>

        <label class="block" for="organizer">
          <span class="text-sm text-gray-700">Organizer</span>
          <input
            type="text"
            v-model="event.organizer"
            required
            id="organizer"
            name="organizer"
             autocomplete="off"
            class="mt-1 block w-full border rounded-md px-3 py-2 shadow-sm"
          />
        </label>

        <label class="block" for="image">
          <span class="text-sm text-gray-700">Image</span>
          <input
            type="file"
            id="image"
            name="image"
             autocomplete="off"
            @change="handleFileChange"
            class="mt-1 block w-full border rounded-md px-3 py-2 shadow-sm"
          />
        </label>

        <button
          class="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700" id="button"
        >
          Update
        </button>
      </form>
    </div>
  </div>
</template>


<script>
import { ref, watch} from 'vue'; 
import api from '../axios';
export default {
  props: {
    event: {
      type: Object,
      required: true
    }
  },
  mounted() {
   document.body.classList.add('overflow-hidden');
  },
  unmounted() {
    document.body.classList.remove('overflow-hidden');
  },
  setup(props, { emit }) {
    const event = ref({
      name: '',
      description: '',
      date: '',
      time: '',
      location: '',
      capacity: 0,
      organizer: '',
      image: null
    });
    

    const errormessage = ref('');
    const messagee = ref('');
    const addextraseats = ref(0);

    watch(() => props.event, (newData) => {
      if (newData) {
       
        event.value = { ...newData}; 
      }
    }, { immediate: true });

    const handleFileChange = (e) => {
      event.value.image = e.target.files[0];
    };

    const handleUpdate = async () => {
      errormessage.value = '';
      messagee.value = '';
      
      event.value.capacity = Number(event.value.capacity) + Number(addextraseats.value);
      

      const formData = new FormData();
      for (const key in event.value) {
        if(key !== 'image')
          formData.append(key, event.value[key]);
      }

      if(event.value.image instanceof File){
        formData.append('image',event.value.image);
      }

      try {
        const response = await api.patch('/events/update-events',formData,
         { headers: { "Content-Type": "multipart/form-data" } }
      );
       
        if (response.status !== 200) {
          throw new Error('Failed to update event');
        }

        messagee.value = 'Event updated successfully!';
        emit("update", response.data.event);
      } catch (error) {
        errormessage.value = error.message;
      }
    };

    return {
      event,
      errormessage,
      addextraseats, 
      messagee,
      handleFileChange,
      handleUpdate
    };
  }
};

</script>
