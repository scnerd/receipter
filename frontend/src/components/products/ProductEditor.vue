<template>
  <Editor
    :object="product"
    :store="productStore"
    :mutator="mutator"
    @update:object="$emit('update:product', product)">
    <v-text-field label="Name" v-model="product.name" type="text"/>
    <v-text-field label="Variant" v-model="product.variant" type="text"/>
    <CategorySelector :id="product.category"
                      @update:modelValue="u => productStore.update(product.id, { category: u.id})"
    ></CategorySelector>
    <BrandSelector :id="product.brand"
                   @update:modelValue="u => productStore.update(product.id, { brand: u.id})"/>

    <UnitSelector :id="product.package_unit"
                  @update:modelValue="u => productStore.update(product.id, { package_unit: u.id})"/>
    <v-text-field label="Quantity" v-model.lazy="product.package_quantity" type="number" step="0.001"/>
    <v-text-field label="Packaging" v-model.lazy="product.package_type" type="text"/>
  </Editor>
</template>

<script setup lang="ts">

import {useProductStore} from "@/store/app";
import UnitSelector from "@/components/units/UnitSelector.vue";
import Editor from "@/components/generic/Editor.vue";
import BrandSelector from "@/components/brands/BrandSelector.vue";
import CategorySelector from "@/components/categories/CategorySelector.vue";

const props = defineProps(["product"])

const productStore = useProductStore()

function mutator(obj) {
  return {
    id: obj.id,
    name: obj.name,
    variant: obj.variant,
    brand: obj.brand,
    package_unit: obj.package_unit,
    package_quantity: obj.package_quantity,
    package_type: obj.package_type,
  }
}
</script>
