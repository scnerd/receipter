<template>
  <v-dialog v-model="showDialog" persistent transition="dialog-bottom-transition" width="1000">
    <template v-slot:activator="{ props }">
      <v-btn v-bind="props" min-width="32" width="32" height="32" variant="tonal">
        <v-icon icon="mdi-pencil-outline"></v-icon>
      </v-btn>
    </template>

    <v-card>
      <v-card-title>Edit Product</v-card-title>
      <v-card-text>
        <v-form>
          <v-text-field label="Name" v-model="product.name" type="text"/>
          <v-text-field label="Variant" v-model="product.variant" type="text"/>
          <BrandSelector label="Brand" v-model="product.brand"
                         @update:modelValue="u => product.brand = u"/>

          <UnitSelector label="Unit" v-model="product.package_unit"
                        @update:modelValue="u => product.package_unit = u"/>
          <v-text-field label="Quantity" v-model.lazy="product.package_quantity" type="number" step="0.001"/>
          <v-text-field label="Packaging" v-model.lazy="product.package_type" type="text"/>

          <v-btn-group width="100%">
            <v-btn @click="showDialog = false" color="red">Cancel</v-btn>
            <v-btn @click="submit" color="blue">Submit</v-btn>
          </v-btn-group>
        </v-form>
        <v-progress-linear v-if="submitting" indeterminate></v-progress-linear>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">

import {ref} from "vue";
import {useProductStore} from "@/store/app";
import BrandSelector from "@/components/brands/BrandSelector.vue";
import UnitSelector from "@/components/units/UnitSelector.vue";

const props = defineProps(["product"])
const emits = defineEmits(["update:product"])

const productStore = useProductStore()
const showDialog = ref(false)
const submitting = ref(false)

async function submit(event) {
  submitting.value = true
  let response = await productStore.update({
    id: props.product.id,
    name: props.product.name,
    variant: props.product.variant,
    brand_id: (props.product.brand ?? {id: null}).id,
    package_unit: (props.product.package_unit ?? {id: null}).id,
    // package_unit: props.product.package_unit,
    package_quantity: props.product.package_quantity,
    package_type: props.product.package_type,
  })
  emits('update:product', response)
  submitting.value = false
  showDialog.value = false
}
</script>
