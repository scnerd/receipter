<template>
  <Editor
    title="Edit Brand"
    :object="brand"
    :store="brandStore"
    :mutator="(x: any) => x"
    @update:object="$emit('update:brand', brand)"
  >
    <template v-slot:default="s">
      <v-text-field v-model="s.object.name" type="text" label="Name"></v-text-field>
    </template>
  </Editor>
</template>

<script setup lang="ts">

import {useBrandStore} from "@/store/app";
import Editor from "@/components/generic/Editor.vue";

const props = defineProps(["brand"])

const brandStore = useBrandStore()
</script>
