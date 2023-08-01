<template>
  <Selector
    :id="brand"
    :store="brandStore"
    :allow-clear="true"
    :allow-delete="true"
    title-attr="name"
    label="Brand"
    >
    <template v-slot:create="s"><BrandCreator @create:brand="v => brand = v"></BrandCreator></template>
    <template v-slot:edit="s"><BrandEditor :brand="s.object"></BrandEditor></template>
  </Selector>
</template>

<script setup lang="ts">
import {useBrandStore} from "@/store/app";
import {computed, ref} from "vue";
import BrandCreator from "@/components/brands/BrandCreator.vue";
import Selector from "@/components/generic/Selector.vue";
import BrandEditor from "@/components/brands/BrandEditor.vue";

const props = defineProps(['modelValue'])

const emit = defineEmits(["update:modelValue"])

const brandStore = useBrandStore()

const brand = computed({
  get() {
    return props.modelValue;
  },
  set(e) {
    emit('update:modelValue', e);
  }
})

// const newBrandName = ref("")
// const creatingBrand = ref(false)

// async function createNewBrand() {
//   if (newBrandName.value) {
//     newBrandName.value = ""
//     creatingBrand.value = true
//
//     const newBrand = await brandStore.createNewBrand(newBrandName.value)
//     selectedBrand.value = newBrand
//     creatingBrand.value = false
//   }
// }
</script>
