<template>
  <v-progress-circular v-if="!productStore.initialized" indeterminate/>
  <v-autocomplete v-else v-model="product" :items="productStore.products" item-title="pretty_name" item-value="id"
                  label="Product"
                  return-object single-line>
    <template v-slot:append>
      <v-btn-group class="align-center">
        <ProductEditor :product="product" @update:product="p => product = p"></ProductEditor>
      </v-btn-group>
    </template>
  </v-autocomplete>
</template>

<script setup lang="ts">
import {useProductStore} from "@/store/app";
import {computed, ref} from "vue";
import ProductEditor from "@/components/products/ProductEditor.vue";
import BrandCreator from "@/components/brands/BrandCreator.vue";

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

// const newProductName = ref("")
// const creatingProduct = ref(false)

// async function createNewProduct() {
//   if (newProductName.value) {
//     newProductName.value = ""
//     creatingProduct.value = true
//
//     const newProduct = await productStore.createNewProduct(newProductName.value)
//     selectedProduct.value = newProduct
//     creatingProduct.value = false
//   }
// }
</script>
