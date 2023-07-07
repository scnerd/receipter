<template>
<v-list-item
  :title="line_item.product.name"
>
  {{ priceLine }}
</v-list-item>
</template>

<script setup lang="ts">
import {computed} from "vue";

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
