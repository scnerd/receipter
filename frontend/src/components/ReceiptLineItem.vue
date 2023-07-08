<template>
<!--  <v-container>-->
      <v-form style="width:100%">
        <v-row>
          <v-col col="2">
            <v-text-field label="Product" v-model="line_item.product.name"/>
          </v-col>
          <v-col col="2">
            <v-text-field label="Quantity" v-model="line_item.quantity"/>
          </v-col>
          <v-col col="2">
            <UnitSelector label="Unit" :unit="line_item.unit"/>
          </v-col>
          <v-col col="2">
            <v-text-field label="Unit Price ($)" v-model="line_item.unit_price"/>
          </v-col>
          <v-col col="2">
            <v-text-field label="Total Price ($)" v-model="line_item.price"/>
          </v-col>
        </v-row>
        <!--    <v-container>-->
        <!--      <v-row>-->
        <!--    <ReceiptLineItemField-->
        <!--      :line_item_id="line_item.id"-->
        <!--      field="quantity"-->
        <!--      :value="line_item.quantity"-->
        <!--      cols="2"-->
        <!--    />-->

        <!--    <ReceiptLineItemField-->
        <!--      :line_item_id="line_item.id"-->
        <!--      field="unit"-->
        <!--      :value="line_item.unit == null ? null : line_item.unit.name"-->
        <!--      cols="2"-->
        <!--    />-->

        <!--    <ReceiptLineItemField-->
        <!--      :line_item_id="line_item.id"-->
        <!--      field="unit_price"-->
        <!--      :value="line_item.unit_price"-->
        <!--      cols="2"-->
        <!--    />-->

        <!--    <ReceiptLineItemField-->
        <!--      :line_item_id="line_item.id"-->
        <!--      field="unit_price"-->
        <!--      :value="line_item.unit_price"-->
        <!--      cols="2"-->
        <!--    />-->

        <!--    <ReceiptLineItemField-->
        <!--      :line_item_id="line_item.id"-->
        <!--      field="total_price"-->
        <!--      :value="line_item.total_price"-->
        <!--      cols="2"-->
        <!--    />-->
        <!--      </v-row>-->
        <!--    </v-container>-->
      </v-form>
<!--  </v-container>-->
</template>

<script setup lang="ts">
import {computed} from "vue";
import UnitSelector from "@/components/UnitSelector.vue";

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
