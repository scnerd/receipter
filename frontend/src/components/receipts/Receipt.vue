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
                <StoreSelector :id="receipt.location_detail.store" @update:model-value="v => locationStore.update({id: receipt.location, store: v.id})"></StoreSelector>
              </v-col>
              <v-col cols="3">
                <LocationSelector :id="receipt.location" @update:model-value="v => receiptStore.update(receipt.id, { location: v.id})"></LocationSelector>
              </v-col>
              <v-col cols="3">
                <EditorLiveField :store="receiptStore" :object="receipt" attribute="date" type="date" label="Date"></EditorLiveField>
              </v-col>
              <v-col cols="3">
                <EditorLiveField :store="receiptStore" :object="receipt" attribute="total_paid" type="number" label="Total" prefix="$"></EditorLiveField>
              </v-col>
            </v-row>
          </v-form>
        </v-row>
        <v-row>
          <!--Receipt image-->
          <v-col cols="4">
            <v-img :src="receipt.source.image_file" alt="Image of receipt"></v-img>
          </v-col>
          <!--Receipt line items-->
          <v-col col="8">
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
import StoreSelector from "@/components/stores/StoreSelector.vue";
import LocationSelector from "@/components/locations/LocationSelector.vue";
import {useLocationStore, useReceiptStore} from "@/store/app";
import EditorLiveField from "@/components/generic/EditorLiveField.vue";

const props = defineProps(["receipt"])
const receiptStore = useReceiptStore()
const locationStore = useLocationStore()

const title = computed(() => {
  return `${props.receipt.date} - ${props.receipt.location_detail.store_detail.name} ($ ${props.receipt.total_paid})`
})

async function deleteReceipt() {
  await fetch(
    `http://localhost:9000/api/receipts/${props.receipt.id}/`,
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
