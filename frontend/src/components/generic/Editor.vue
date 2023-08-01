<template>
  <v-dialog v-model="showDialog" persistent transition="dialog-bottom-transition" width="1000">
    <template v-slot:activator="{ props }">
      <slot name="activator" v-bind="props">
        <v-btn v-bind="props" color="blue" min-width="32" width="32" height="32" variant="tonal">
          <v-icon icon="mdi-pencil-outline"></v-icon>
        </v-btn>
      </slot>
    </template>

    <v-card>
      <v-card-title>{{ title }}</v-card-title>
      <v-card-text>
        <v-form>
          <slot :object="object"></slot>

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

const props = defineProps(["object", "title", "store", "mutator"])
const emits = defineEmits(["update:object"])

const showDialog = ref(false)
const submitting = ref(false)

async function submit(event) {
  submitting.value = true
  let mutator = props.mutator ?? ((x: object) => x)
  let result = await props.store.update(mutator(props.object))
  emits("update:object", result)
  submitting.value = false
  showDialog.value = false
}
</script>
