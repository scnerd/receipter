<template>
  <Selector
    v-model="store"
    :store="storeStore"
    :allow-clear="true"
    :allow-delete="true"
    title-attr="name"
    label="Store"
    >
    <template v-slot:edit="s"><StoreEditor :store="s.object"></StoreEditor></template>
  </Selector>
</template>

<script setup lang="ts">
import {useStoreStore} from "@/store/app";
import {computed, ref} from "vue";
import Selector from "@/components/generic/Selector.vue";
import StoreEditor from "@/components/stores/StoreEditor.vue";

const props = defineProps(['modelValue'])

const emit = defineEmits(["update:modelValue"])

const storeStore = useStoreStore()

const store = computed({
  get() {
    return props.modelValue;
  },
  set(e) {
    emit('update:modelValue', e);
  }
})

// const newStoreName = ref("")
// const creatingStore = ref(false)

// async function createNewStore() {
//   if (newStoreName.value) {
//     newStoreName.value = ""
//     creatingStore.value = true
//
//     const newStore = await storeStore.createNewStore(newStoreName.value)
//     selectedStore.value = newStore
//     creatingStore.value = false
//   }
// }
</script>
