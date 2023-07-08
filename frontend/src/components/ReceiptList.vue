<template>
  <v-container class="text-center">
    <v-row>
      <v-btn-group>
        <v-btn color="primary" :block="true" variant="outlined" @click="showFileInput = !showFileInput">Scan New
          Receipt
        </v-btn>
      </v-btn-group>
      <v-file-input v-if="showFileInput" accept="image/*" v-model="file" @change="onFileChange"></v-file-input>
      <v-progress-linear v-if="uploadingReceipt" v-model="uploadingReceiptProgress"></v-progress-linear>
    </v-row>
    <v-row>
      <v-progress-circular v-if="!receipts" indeterminate color="primary"></v-progress-circular>
      <v-expansion-panels v-else>
        <Receipt
          v-for="receipt in receipts"
          :key="receipt.id"
          :receipt="receipt"
        />
      </v-expansion-panels>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import {ref} from 'vue'
import Receipt from './Receipt.vue'
import {handleErrors} from "@/utils";

const receipts = ref(null)
const showFileInput = ref(false)
const file = ref(null)
const uploadingReceipt = ref(false)
const uploadingReceiptProgress = ref(0)

fetch('http://localhost:8000/api/receipts/')
  .then(response => response.json())
  .then(data => receipts.value = data.results)

async function onFileChange(e) {
  showFileInput.value = false
  uploadingReceipt.value = true
  uploadingReceiptProgress.value = 0

  let formdata = new FormData();
  formdata.append("image_file", e.target.files[0]);

  let requestOptions = {
    method: 'POST',
    body: formdata,
  };

  let receipt_file = await fetch("http://localhost:8000/api/receipt-files/", requestOptions)
    .then(handleErrors)
    .then(response => response.json())

  let analysis_result = await fetch(`http://localhost:8000/api/receipt-files/${receipt_file.id}/analyze/`, {method: 'POST'})
    .then(handleErrors)
    .then(response => response.json())

  let new_receipt = await fetch(`http://localhost:8000/api/receipts/${analysis_result.receipt_id}/`)
    .then(handleErrors)
    .then(response => response.json())

  receipts.value.unshift(new_receipt)
}
</script>
