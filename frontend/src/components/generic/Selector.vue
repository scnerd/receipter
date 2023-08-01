<template>
  <v-progress-circular v-if="!store.initialized" indeterminate/>
  <v-autocomplete v-else v-model="obj" :items="store.objectList" :item-title="titleAttr || 'name'" item-value="id"
                  :label="label"
                  return-object single-line auto-select-first>
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
    <!--    <template v-slot:message>-->
    <!--      <v-progress-linear indeterminate v-if="emitting"></v-progress-linear>-->
    <!--    </template>-->
  </v-autocomplete>
</template>

<script setup lang="ts">
import {computed} from "vue";

// const props = defineProps(['id', 'store', 'allowClear', 'allowDelete', 'titleAttr', 'label'])
const props = defineProps<{
  id: string,
  store: any,
  allowClear: boolean,
  allowDelete: boolean,
  titleAttr: string,
  label: string
  parentStore?: any
  parentId?: number
  parentAttr?: string
}>()

const emit = defineEmits(["update:modelValue"])

const canSetParent = computed(() => props.parentStore != null && props.parentId != null && props.parentAttr != null)

const obj = computed({
  get() {
    return props.store.objects.get(props.id)
  },
  set(e) {
    emit('update:modelValue', e);
    if (canSetParent.value) {
      props.parentStore.update(props.parentId, {[props.parentAttr]: e})
    }
  }
})

async function deleteObj() {
  await props.store.delete_(obj.value.id)
  obj.value = null
}
</script>
