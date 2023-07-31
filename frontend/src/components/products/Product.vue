<template>
  <v-form>
    <v-row>
      <v-col cols="2">
        <v-text-field label="Name" v-model="product.name" type="text"
                      @change="patchField('products', product.id, 'name', $event.target.value)"/>
      </v-col>
      <v-col cols="2">
        <v-text-field label="Variant" v-model="product.variant" type="text"
                      @change="patchField('products', product.id, 'variant', $event.target.value)"/>
      </v-col>
      <v-col cols="2">
        <BrandSelector label="Brand" v-model="product.brand_detail"
                       @update:modelValue="u => patchField('products', product.id, 'brand', (u ?? {id: null}).id)"/>
      </v-col>

      <v-col cols="2">
        <UnitSelector label="Unit" v-model="product.package_unit_detail"
                      @update:modelValue="u => patchField('products', product.id, 'package_unit', (u ?? {id: null}).id)"/>
      </v-col>
      <v-col cols="1">
        <v-text-field label="Quantity" v-model.lazy="product.package_quantity" type="number" step="0.001"
                      @change="patchField('products', product.id, 'package_quantity', $event.target.value)"/>
      </v-col>
      <v-col cols="2">
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

const props = defineProps(['product'])

</script>

