<template>
  <v-progress-circular v-if="!productStore.initialized" indeterminate/>
  <v-container
    v-else
  >
    <Product
      v-for="product in productStore.objectList"
      :key="product.id"
      :product="product"
      ></Product>
  </v-container>
</template>

<script setup lang="ts">
import {useProductStore} from "@/store/app";
import {patchField} from "@/utils";
import Product from "@/components/products/Product.vue"

const productStore = useProductStore()

const headers = [
  {
    title: "Name",
    align: "start",
    sortable: true,
    key: "name",
  },
  {
    title: "Brand",
    align: "start",
    sortable: true,
    key: "brand",
  },
  {
    title: "Packaging",
    align: "start",
    sortable: true,
    key: "packaging",
  }
]
</script>

