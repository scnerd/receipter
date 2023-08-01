<template>
  <Editor
    title="Edit Category"
    :object="category"
    :store="categoryStore"
    :mutator="(x: any) => x"
    @update:object="$emit('update:category', category)"
  >
    <template v-slot:default="s">
      <v-text-field v-model="s.object.name" type="text" label="Name"></v-text-field>
    </template>
  </Editor>
</template>

<script setup lang="ts">

import {useCategoryStore} from "@/store/app";
import Editor from "@/components/generic/Editor.vue";

const props = defineProps(["category"])

const categoryStore = useCategoryStore()
</script>
