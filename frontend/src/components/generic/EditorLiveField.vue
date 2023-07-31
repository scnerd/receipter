<template>
<v-text-field v-model.lazy="object[attribute]" :type="type" :label="label" @update:model-value="store.update({id: object.id, [attribute]: $event.target.value})"></v-text-field>
</template>

<script setup lang="ts">
const props = defineProps({
  store: Object,
  object: Object,
  attribute: String,
  type: String,
  label: String,
})
</script>
