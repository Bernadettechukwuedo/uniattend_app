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
                    <qrcode-stream
                        :constraints="constraints"
                        :track="paintOutline"
                        @detect="onDetect"
                        @init="onInit"
                    />
                            
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
            errormessage:"",
            constraints : { facingMode: 'environment' }
        }
    },
   methods: {
    // Draw red border around detected QR
    paintOutline(detectedCodes, ctx) {
      for (const detectedCode of detectedCodes) {
        const [firstPoint, ...otherPoints] = detectedCode.cornerPoints;
        ctx.strokeStyle = "red";
        ctx.lineWidth = 4;
        ctx.beginPath();
        ctx.moveTo(firstPoint.x, firstPoint.y);
        for (const { x, y } of otherPoints) {
          ctx.lineTo(x, y);
        }
        ctx.lineTo(firstPoint.x, firstPoint.y);
        ctx.closePath();
        ctx.stroke();
      }
    },

    // Called when a QR code is detected
    async onDetect(detectedCode) {
      const code = detectedCode[0]?.rawValue;
      if (!code || this.scannedCode === code) return; // avoid duplicate scans
      this.scannedCode = code;
      console.log("Scanned QR Code:", code);

      try {
        const response = await api.post("/registration/validate-qr", {
          qr_code: code,
        });

        if (response.data.success) {
          this.successmessage = "Check-in successful!";
          this.errormessage = "";
          this.$emit("success", code);
        } else {
          this.errormessage = " Invalid or already checked in.";
          this.successmessage = "";
        }
      } catch (error) {
        console.error(error);
        this.errormessage = "Error validating QR code.";
        this.successmessage = "";
      }

      setTimeout(() => {
        this.successmessage = "";
        this.errormessage = "";
        this.scannedCode = null;
      }, 2000);
    },

    onInit(promise) {
      promise
        .then(() => console.log("Camera initialized successfully"))
        .catch((error) => {
          console.error("Camera init error:", error);
          this.errormessage = "Unable to access camera. Please allow permissions.";
        });
    },
  },
    mounted(){
    document.body.classList.add("overflow-hidden")
},
unmounted(){
    document.body.classList.remove("overflow-hidden")

}
}




</script>
