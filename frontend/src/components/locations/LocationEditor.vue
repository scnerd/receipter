<template>
  <Editor
    title="Edit Location"
    :object="location"
    :store="locationStore"
    :mutator="(x: any) => x"
    @update:object="$emit('update:location', location)"
  >
    <template v-slot:default="s">
      <v-text-field v-model="s.object.name" type="text" label="Name"></v-text-field>
      <StoreSelector :id="s.object.store" @update:model-value="v => location.store = v"></StoreSelector>
    </template>
  </Editor>
</template>

<script setup lang="ts">

import {useLocationStore} from "@/store/app";
import Editor from "@/components/generic/Editor.vue";
import StoreSelector from "@/components/stores/StoreSelector.vue";

const props = defineProps(["location"])

const locationStore = useLocationStore()
</script>
