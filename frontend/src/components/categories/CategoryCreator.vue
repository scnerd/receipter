<template>
  <Creator
    title="New Category"
    :store="categoryStore"
    :mutator="(x: any) => x"
    @create:object="$emit('create:category', $event)"
  >
    <template v-slot:default="s">
      <v-text-field v-model="s.object.name" type="text" label="Name"></v-text-field>
    </template>
  </Creator>
</template>

<script setup lang="ts">

import {Ref, ref} from "vue";
import {ProductCategory, useCategoryStore} from "@/store/app";
import Creator from "@/components/generic/Creator.vue";

const categoryStore = useCategoryStore()

const category: Ref<ProductCategory> = ref({
  id: null,
  name: null
})
</script>
