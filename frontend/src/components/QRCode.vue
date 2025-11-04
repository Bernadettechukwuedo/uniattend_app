<template>
        <div class="fixed inset-0 z-50 flex justify-center items-center bg-black/80">
            <div v-if="successmessage" class="text-green-500 text-center mb-4">{{ successmessage }}</div>
            <div v-if="errormessage" class="text-red-500 text-center mb-4">{{ errormessage }}</div>
            <div class="relative max-w-md max-h-fit mx-4 p-6 bg-white rounded-lg shadow-lg" >
                                  <button
                    @click="$emit('cancel')"
                    class="absolute top-3 right-3 text-gray-500 hover:text-gray-700"
                >
                    ✕
                </button>
                <h1>Scanned {{ scannedCode }}</h1>

                <qrcode-stream @decode="onDetect" ></qrcode-stream>
            
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
            successmessage:"",
            errormessage:""
        }
    },
    methods:{
        async onDetect(code) {
            if (this.scannedCode == code) return;
            this.scannedCode = code;
            console.log('Scanned QR Code:', code);
            const response = await api.post('/registration/validate-qr', {
                qr_code: code
            });
            console.log(response.data);
            if(response.data.success){
                this.successmessage = 'Check-in successful!';
                this.errormessage=""
                this.$emit('success', code);
                setTimeout(() => {
                    
                    this.successmessage = '';
                    this.scannedCode = null;
                }, 2000);
            } else {

                this.errormessage ='Invalid QR code or already checked in.';
                this.successmessage=""
                setTimeout(() => {
                    this.errormessage = '';
                    this.scannedCode = null;
                }, 2000);
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
