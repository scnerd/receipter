<template>
  <v-progress-circular v-if="!unitStore.initialized" indeterminate/>
  <v-select v-else v-model="unit" :items="unitStore.units" item-title="name" item-value="id" label="name"
            return-object single-line>
<!--    <template v-slot:prepend-item>-->
<!--      <v-list-item title="Create new unit">-->
<!--        <template v-slot:append>-->
<!--          <v-row>-->
<!--            <v-col col="auto">-->
<!--              <v-text-field v-model="newUnitName" placeholder="New unit name..."-->
<!--                            :disabled="creatingUnit"></v-text-field>-->
<!--            </v-col>-->
<!--            <v-col>-->
<!--              <v-btn color="primary" @click="createNewUnit">-->
<!--                <v-progress-circular v-if="creatingUnit" indeterminate/>-->
<!--                <span v-else>+</span>-->
<!--              </v-btn>-->
<!--            </v-col>-->
<!--          </v-row>-->
<!--        </template>-->
<!--      </v-list-item>-->
<!--    </template>-->
  </v-select>
</template>

<script setup lang="ts">
import {useUnitsStore} from "@/store/units";
import {ref} from "vue";

const props = defineProps({
  modelValue: String,
  unit: String,
})

// const newUnitName = ref("")
// const creatingUnit = ref(false)

const unitStore = useUnitsStore()

defineEmits(["update:modelValue"])

// async function createNewUnit() {
//   if (newUnitName.value) {
//     newUnitName.value = ""
//     creatingUnit.value = true
//
//     const newUnit = await unitStore.createNewUnit(newUnitName.value)
//     selectedUnit.value = newUnit
//     creatingUnit.value = false
//   }
// }
</script>
