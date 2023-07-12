<template>
  <v-expansion-panel
    :key="receipt.id"
    v-bind="props"
    :title="title"
  >
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
                />
              </v-col>
              <v-col cols="3">
                <v-text-field
                  v-model="receipt.total_paid"
                  label="Total"
                  type="number"
                  prefix="$"
                  step="0.01"
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

const props = defineProps(["receipt"])

const title = computed(() => {
  return `${props.receipt.date} - ${props.receipt.location.store.name} ($ ${props.receipt.total_price})`
})
</script>
