<template>
  <Editor
    title="Edit Unit"
    :object="unit"
    :store="unitStore"
    :mutator="(x: any) => x"
    @update:object="$emit('update:unit', unit)"
  >
    <template v-slot:default="s">
      <v-text-field v-model="s.object.name" type="text" label="Name"></v-text-field>
    </template>
  </Editor>
</template>

<script setup lang="ts">

import {useUnitStore} from "@/store/app";
import Editor from "@/components/generic/Editor.vue";

const props = defineProps(["unit"])

const unitStore = useUnitStore()
</script>
