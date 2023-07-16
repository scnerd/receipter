<template>
  <v-form style="width:100%">
    <v-row>
      <v-col col="2">
        <v-text-field label="Product" v-model="line_item.product.pretty_name" type="text"/>
      </v-col>
      <v-col col="2">
        <v-text-field label="Quantity" v-model="line_item.quantity" type="number" step="0.001"
                      @change="patchField('line-items', line_item.id, 'quantity', $event.target)"/>
      </v-col>
      <v-col col="2">
        <UnitSelector label="Unit" v-model:unit="line_item.unit"/>
      </v-col>
      <v-col col="2">
        <v-text-field label="Unit Price" v-model="line_item.unit_price" prefix="$" type="number" step="0.01"
                      @change="patchField('line-items', line_item.id, 'unit_price', $event.target)"/>
      </v-col>
      <v-col col="2">
        <v-text-field label="Total Price" v-model="line_item.price" prefix="$" type="number" step="0.01"
                      @change="patchField('line-items', line_item.id, 'price', $event.target)"/>
      </v-col>
    </v-row>
  </v-form>
</template>

<script setup lang="ts">
import {computed} from "vue";
import UnitSelector from "@/components/UnitSelector.vue";
import {patchField} from "@/utils";

const props = defineProps(["line_item"])

const priceLine = computed(() => {
  let unit = props.line_item.unit == null ? "" : props.line_item.unit.name

  let quantity = props.line_item.quantity == null ? 1 : props.line_item.quantity

  let unit_price = props.line_item.unit_price == null ? props.line_item.price / quantity : props.line_item.unit_price

  let quantity_text = ""
  let unit_price_text = ""

  if (unit != "") {
    quantity_text = `${quantity} ${unit}`
    unit_price_text = `\$${unit_price} / ${unit}`
  } else {
    quantity_text = `${quantity}`
    unit_price_text = `\$${unit_price}`
  }

  if (quantity != "1") {
    return `${quantity_text} @ ${unit_price_text} = \$${props.line_item.price}`
  } else {
    return `\$${props.line_item.price}`
  }
})
</script>
