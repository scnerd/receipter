<template>
  <Creator
    title="New Unit"
    :store="unitStore"
    :mutator="(x: any) => x"
    @create:object="$emit('create:unit', $event)"
  >
    <template v-slot:default="s">
      <v-text-field v-model="s.object.name" type="text" label="Name"></v-text-field>
    </template>
  </Creator>
</template>

<script setup lang="ts">

import {Ref, ref} from "vue";
import {Unit, useUnitStore} from "@/store/app";
import Creator from "@/components/generic/Creator.vue";

const unitStore = useUnitStore()

const unit: Ref<Unit> = ref({
  id: null,
  name: null
})
</script>
