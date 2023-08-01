<template>
  <Selector
    v-model="unit"
    :store="unitStore"
    :allow-clear="true"
    :allow-delete="true"
    title-attr="name"
    label="Unit"
    >
    <template v-slot:create="s"><UnitCreator @create:unit="v => unit = v"></UnitCreator></template>
    <template v-slot:edit="s"><UnitEditor :unit="s.object"></UnitEditor></template>
  </Selector>
</template>

<script setup lang="ts">
import {useUnitStore} from "@/store/app";
import {computed, ref} from "vue";
import UnitCreator from "@/components/units/UnitCreator.vue";
import Selector from "@/components/generic/Selector.vue";
import UnitEditor from "@/components/units/UnitEditor.vue";

const props = defineProps(['modelValue'])

const emit = defineEmits(["update:modelValue"])

const unitStore = useUnitStore()

const unit = computed({
  get() {
    return props.modelValue;
  },
  set(e) {
    emit('update:modelValue', e);
  }
})

// const newUnitName = ref("")
// const creatingUnit = ref(false)

// async function createNewUnit() {
//   if (newUnitName.value) {
//     newUnitName.value = ""
//     creatingUnit.value = true
//
//     const newUnit = await unitStore.createNewUnit(newUnitName.value)
//     selectedUnit.value = newUnit
//     creatingUnit.value = false
//   }
// }
</script>
