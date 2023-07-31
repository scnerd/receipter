<template>
  <Creator
    title="New Brand"
    :store="brandStore"
    :mutator="(x: any) => x"
    @create:object="$emit('create:brand', $event)"
  >
    <template v-slot:default="s">
      <v-text-field v-model="s.object.name" type="text" label="Name"></v-text-field>
    </template>
  </Creator>
</template>

<script setup lang="ts">

import {Ref, ref} from "vue";
import {Brand, useBrandStore} from "@/store/app";
import Creator from "@/components/generic/Creator.vue";

const brandStore = useBrandStore()

const brand: Ref<Brand> = ref({
  id: null,
  name: null
})
</script>
