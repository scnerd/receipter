<template>
  <Editor
    title="Edit Store"
    :object="store"
    :store="storeStore"
    :mutator="(x: any) => x"
    @update:object="$emit('update:store', store)"
  >
    <template v-slot:default="s">
      <v-text-field v-model="s.object.name" type="text" label="Name"></v-text-field>
    </template>
  </Editor>
</template>

<script setup lang="ts">

import {useStoreStore} from "@/store/app";
import Editor from "@/components/generic/Editor.vue";

const props = defineProps(["store"])

const storeStore = useStoreStore()
</script>
