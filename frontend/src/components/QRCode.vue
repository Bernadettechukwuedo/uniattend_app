<template>
        <div class="fixed inset-0 z-50 flex justify-center items-center bg-black/80">
            <div class="relative max-w-md max-h-fit mx-4 p-6 bg-white rounded-lg shadow-lg" >
                                  <button
                    @click="$emit('cancel')"
                    class="absolute top-3 right-3 text-gray-500 hover:text-gray-700"
                >
                    ✕
                </button>
                <h1>Scanned {{ scannedCode }}</h1>

                <qrcode-stream @decode="onDetect"></qrcode-stream>
            
                </div>
            
        </div>
</template>

<script>
import api from '../axios';
import { QrcodeStream} from 'vue-qrcode-reader'
export default{
    components: {
        QrcodeStream,
    },
    data(){
        return{
            scannedCode: null,
        }
    },
    methods:{
        async onDetect(code) {
            this.scannedCode = code;
            console.log('Scanned QR Code:', code);
            const response = await api.post(`${import.meta.env.VITE_API_BASE_URL}/registration/validate-qr`, {
                qr_code: code
            });
            console.log(response.data);
            if(response.data.success){
                alert('Check-in successful!');
            } else {
                alert('Invalid QR code or already checked in.');
            }
          }
    },
    mounted(){
    document.body.classList.add("overflow-hidden")
},
unmounted(){
    document.body.classList.remove("overflow-hidden")

}
}




</script>
