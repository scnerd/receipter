<template>
  <Selector
    v-model="location"
    :store="locationStore"
    :allow-clear="true"
    :allow-delete="true"
    title-attr="name"
    label="Location"
    >
    <template v-slot:edit="s"><LocationEditor :location="s.object"></LocationEditor></template>
  </Selector>
</template>

<script setup lang="ts">
import {useLocationStore} from "@/store/app";
import {computed, ref} from "vue";
import Selector from "@/components/generic/Selector.vue";
import LocationEditor from "@/components/locations/LocationEditor.vue";

const props = defineProps(['modelValue'])

const emit = defineEmits(["update:modelValue"])

const locationStore = useLocationStore()

const location = computed({
  get() {
    return props.modelValue;
  },
  set(e) {
    emit('update:modelValue', e);
  }
})

// const newLocationName = ref("")
// const creatingLocation = ref(false)

// async function createNewLocation() {
//   if (newLocationName.value) {
//     newLocationName.value = ""
//     creatingLocation.value = true
//
//     const newLocation = await locationStore.createNewLocation(newLocationName.value)
//     selectedLocation.value = newLocation
//     creatingLocation.value = false
//   }
// }
</script>
