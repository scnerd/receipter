<template>
  <Selector
    v-model="product"
    :store="productStore"
    :allow-clear="true"
    :allow-delete="true"
    title-attr="name"
    label="Product"
    >
    <template v-slot:edit="s"><ProductEditor :product="s.object"></ProductEditor></template>
  </Selector>
</template>

<script setup lang="ts">
import {useProductStore} from "@/store/app";
import {computed, ref} from "vue";
import Selector from "@/components/generic/Selector.vue";
import ProductEditor from "@/components/products/ProductEditor.vue";

const props = defineProps(['modelValue'])

const emit = defineEmits(["update:modelValue"])

const productStore = useProductStore()

const product = computed({
  get() {
    return props.modelValue;
  },
  set(e) {
    emit('update:modelValue', e);
  }
})
</script>
