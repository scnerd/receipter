<template>
  <v-progress-circular v-if="!store.initialized" indeterminate/>
  <v-autocomplete v-else v-model="obj" :items="store.objectList" :item-title="titleAttr || 'name'" item-value="id"
                  :label="label"
                  return-object single-line>
    <template v-slot:append>
      <v-btn-group class="align-center">
        <slot name="create" :object="obj"></slot>
        <slot v-if="obj != null" name="edit" :object="obj"></slot>
        <v-btn v-if="obj != null && allowClear" color="purple" @click="obj = null" min-width="32" width="32" height="32"
               variant="tonal">
          <v-icon icon="mdi-eraser"></v-icon>
        </v-btn>
        <v-btn v-if="obj != null && allowDelete" color="red" @click="deleteObj" min-width="32" width="32" height="32"
               variant="tonal">
          <v-icon icon="mdi-trash-can-outline"></v-icon>
        </v-btn>
      </v-btn-group>
    </template>
  </v-autocomplete>
</template>

<script setup lang="ts">
import {computed} from "vue";

const props = defineProps(['modelValue', 'store', 'allowClear', 'allowDelete', 'titleAttr', 'label'])

const emit = defineEmits(["update:modelValue"])

const obj = computed({
  get() {
    return props.modelValue;
  },
  set(e) {
    emit('update:modelValue', e);
  }
})

async function deleteObj() {
  await props.store.delete_(obj.value.id)
  obj.value = null
}
</script>
