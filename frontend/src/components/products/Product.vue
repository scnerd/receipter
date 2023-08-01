<template>
  <v-form>
    <v-row>
      <v-col cols="2">
        <v-text-field label="Name" v-model="product.name" type="text"
                      @change="patchField('products', product.id, 'name', $event.target.value)"/>
      </v-col>
      <v-col cols="1">
        <v-text-field label="Variant" v-model="product.variant" type="text"
                      @change="patchField('products', product.id, 'variant', $event.target.value)"/>
      </v-col>
      <v-col cols="2">
        <CategorySelector :parent-store="productStore" :parent-id="product.id" parent-attr="category"/>
      </v-col>
      <v-col cols="2">
        <BrandSelector v-model="product.brand"
                       @update:modelValue="u => productStore.update(product.id, {brand: u})"/>
      </v-col>
      <v-col cols="2">
        <UnitSelector v-model="product.package_unit"
                      @update:modelValue="u => productStore.update(product.id, {package_unit: u})"/>
      </v-col>
      <v-col cols="1">
        <v-text-field label="Quantity" v-model.lazy="product.package_quantity" type="number" step="0.001"
                      @change="patchField('products', product.id, 'package_quantity', $event.target.value)"/>
      </v-col>
      <v-col cols="1">
        <v-text-field label="Packaging" v-model.lazy="product.package_type" type="text"
                      @change="patchField('products', product.id, 'package_type', $event.target.value)"/>
      </v-col>
      <v-col cols="1">
        <ProductInfoDialog :product="product"></ProductInfoDialog>
      </v-col>
    </v-row>
  </v-form>
</template>

<script setup lang="ts">
import {handleErrors, patchField} from "@/utils";
import BrandSelector from "@/components/brands/BrandSelector.vue";
import UnitSelector from "@/components/units/UnitSelector.vue";
import ProductInfoDialog from "@/components/products/ProductInfoDialog.vue";
import {computed, ref} from "vue";
import {useProductStore} from "@/store/app";
import CategorySelector from "@/components/categories/CategorySelector.vue";

const props = defineProps(['product'])
const productStore = useProductStore()

</script>

