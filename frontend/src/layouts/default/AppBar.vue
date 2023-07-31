<template>
  <v-app-bar flat>
    <v-app-bar-title>
      <v-icon icon="mdi-receipt-text"/>

      Receiptster
    </v-app-bar-title>
    <router-link to="/receipts">
      <v-btn variant="outlined">Receipts</v-btn>
    </router-link>
    <router-link to="/products">
      <v-btn variant="outlined">Products</v-btn>
    </router-link>
  </v-app-bar>
</template>

<script lang="ts" setup>
//
</script>
