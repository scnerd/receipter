<template>
  <v-container class="text-center">
    <v-row>
      <v-expansion-panels>
        <v-expansion-panel
          title=""
        >
          <v-expansion-panel-title>
            Scan New Receipt
          </v-expansion-panel-title>
          <v-expansion-panel-text>
            <v-row align="center" justify="center">
              <v-col cols="1">
                <v-progress-circular v-model="uploadingReceiptProgress" indeterminate></v-progress-circular>
              </v-col>
              <v-col cols="11">
                <v-file-input accept="image/*" v-model="file" @change="onFileChange"></v-file-input>
              </v-col>
            </v-row>
          </v-expansion-panel-text>
        </v-expansion-panel>
      </v-expansion-panels>
    </v-row>
    <v-row>
      <v-progress-circular v-if="!receiptStore.initialized" indeterminate color="primary"></v-progress-circular>
      <v-expansion-panels v-else>
        <Receipt
          v-for="receipt in receiptStore.receipts"
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
import {useReceiptsStore} from "@/store/receipts";

const receiptStore = useReceiptsStore()
const showFileInput = ref(false)
const file = ref(null)
const uploadingReceipt = ref(false)
const uploadingReceiptProgress = ref(0)

// fetch('http://localhost:8000/api/receipts/')
//   .then(response => response.json())
//   .then(data => receipts.value = data.results)

async function onFileChange(e) {
  showFileInput.value = false
  uploadingReceipt.value = true
  uploadingReceiptProgress.value = 0

  let formdata = new FormData();
  formdata.append("image_file", e.target.files[0]);

  let analysis_result = await fetch(
    "http://localhost:8000/api/receipt-files/analyze/",
    {method: 'POST', body: formdata}
  )
    .then(handleErrors)
    .then(response => response.json())

  await receiptStore.refresh()

  // let new_receipt = await fetch(
  //   `http://localhost:8000/api/receipts/${analysis_result.receipt_id}/`
  // )
  //   .then(handleErrors)
  //   .then(response => response.json())

  // receipts.value.unshift(new_receipt)

  uploadingReceipt.value = false
}
</script>
