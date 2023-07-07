<template>
  <v-list-group>
    <template v-slot:activator="{ props }">
      <v-list-item
        :key="receipt.id"
        v-bind="props"
        :title="title"
      ></v-list-item>
    </template>

    <ReceiptLineItem
      v-for="line_item in receipt.line_items"
      :key="line_item.id"
      :line_item="line_item"
    />
  </v-list-group>
</template>

<script setup lang="ts">
import {computed} from "vue";
import ReceiptLineItem from "./ReceiptLineItem.vue";

const props = defineProps(["receipt"])

const title = computed(() => {
  return `${props.receipt.date} - ${props.receipt.location.store.name} ($ ${props.receipt.total_price})`
})
</script>
