<template>
  <Editor
    :object="product"
    :store="productStore"
    :mutator="(x: any) => x"
    @update:object="$emit('update:product', product)">
    <v-text-field label="Name" v-model="product.name" type="text"/>
    <v-text-field label="Variant" v-model="product.variant" type="text"/>
    <BrandSelector label="Brand" v-model="product.brand_detail"
                   @update:modelValue="u => product.brand = u"/>

    <UnitSelector label="Unit" v-model="product.package_unit"
                  @update:modelValue="u => product.package_unit = u"/>
    <v-text-field label="Quantity" v-model.lazy="product.package_quantity" type="number" step="0.001"/>
    <v-text-field label="Packaging" v-model.lazy="product.package_type" type="text"/>
  </Editor>
</template>

<script setup lang="ts">

import {ref} from "vue";
import {useProductStore} from "@/store/app";
import ProductSelector from "@/components/products/ProductSelector.vue";
import UnitSelector from "@/components/units/UnitSelector.vue";
import Editor from "@/components/generic/Editor.vue";
import BrandSelector from "@/components/brands/BrandSelector.vue";

const props = defineProps(["product"])
const emits = defineEmits(["update:product"])

const productStore = useProductStore()

function mutator(obj) {
  return {
    id: obj.id,
    name: obj.name,
    variant: obj.variant,
    product_id: (obj.product ?? {id: null}).id,
    package_unit: (obj.package_unit ?? {id: null}).id,
    // package_unit: obj.package_unit,
    package_quantity: obj.package_quantity,
    package_type: obj.package_type,
  }
}
</script>
