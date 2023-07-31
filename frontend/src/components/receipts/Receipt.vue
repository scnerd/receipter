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
                <v-autocomplete
                  v-model="receipt.store_detail.name"
                  :items="storesStore.stores"
                  item-title="name"
                  item-value="id"
                  label="Store"
                  @change="patchField('stores', receipt.store_detail.id, 'name', $event.target.value)"
                />
              </v-col>
              <v-col cols="3">
                <v-text-field
                  v-model.lazy="receipt.location_detail.name"
                  label="Location"
                  @change="patchField('locations', receipt.location_detail.id, 'name', $event.target.value)"
                />
              </v-col>
              <v-col cols="3">
                <v-text-field
                  v-model.lazy="receipt.date"
                  label="Date"
                  type="date"
                  @change="patchField('receipts', receipt.id, 'date', $event.target.value)"
                />
              </v-col>
              <v-col cols="3">
                <v-text-field
                  v-model.lazy="receipt.total_paid"
                  label="Total"
                  type="number"
                  prefix="$"
                  step="0.01"
                  @change="patchField('receipts', receipt.id, 'total_paid', $event.target.value)"
                />
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
import {useStoreStore} from "@/store/app";
import {useLocationStore} from "@/store/app";

const props = defineProps(["receipt"])

const storesStore = useStoreStore()
const locationsStore = useLocationStore()

const title = computed(() => {
  return `${props.receipt.date} - ${props.receipt.store_detail.name} ($ ${props.receipt.total_paid})`
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
