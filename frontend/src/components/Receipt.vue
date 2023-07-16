<template>
  <v-expansion-panel
    :key="receipt.id"
    v-bind="props"
  >
    <v-expansion-panel-title>
      <v-col class="text-left"><span>{{ title }}</span></v-col>
      <v-col class="text-right">
        <v-btn variant="outlined" color="red" @click="deleteReceipt">Delete</v-btn>
      </v-col>
    </v-expansion-panel-title>

    <v-expansion-panel-text>
      <v-container fluid>
        <v-row>
          <v-form style="width:100%">
            <v-row>
              <v-col cols="3">
                <v-text-field
                  v-model="receipt.location.store.name"
                  label="Store"
                />
              </v-col>
              <v-col cols="3">
                <v-text-field
                  v-model="receipt.location.name"
                  label="Location"
                />
              </v-col>
              <v-col cols="3">
                <v-text-field
                  v-model="receipt.date"
                  label="Date"
                  type="date"
                  @update:modelValue="patchField('receipts', receipt.id, 'date', $event.target.value)"
                />
              </v-col>
              <v-col cols="3">
                <v-text-field
                  v-model="receipt.total_paid"
                  label="Total"
                  type="number"
                  prefix="$"
                  step="0.01"
                  @update:modelValue="patchField('receipts', receipt.id, 'total_paid', $event.target.value)"
                />
              </v-col>
            </v-row>
          </v-form>
        </v-row>
        <v-row>
          <!--Receipt image-->
          <v-col cols="5">
            <v-img :src="receipt.source.image_file" alt="Image of receipt"></v-img>
          </v-col>
          <!--Receipt line items-->
          <v-col col="7">
            <v-container fluid>
              <v-row v-for="line_item in receipt.line_items" :key="line_item.id">
                <ReceiptLineItem
                  :line_item="line_item"
                />
              </v-row>
            </v-container>
          </v-col>
        </v-row>
      </v-container>

    </v-expansion-panel-text>
  </v-expansion-panel>
</template>

<script setup lang="ts">
import {computed} from "vue";
import ReceiptLineItem from "./ReceiptLineItem.vue";
import {handleErrors, patchField} from "@/utils";

const props = defineProps(["receipt"])

const title = computed(() => {
  return `${props.receipt.date} - ${props.receipt.location.store.name} ($ ${props.receipt.total_paid})`
})

async function deleteReceipt() {
  await fetch(
    `http://localhost:8000/api/receipts/${props.receipt.id}/`,
    {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json"
      }
    }
  )
    .then(handleErrors);
}
</script>
