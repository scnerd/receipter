<template>
  <v-dialog v-model="showDialog" transition="dialog-bottom-transition" width="1000">
    <template v-slot:activator="{ props }">
      <v-btn v-bind="props" height="70%">
        More Info
      </v-btn>
    </template>

    <v-card>
      <v-card-title>Info for {{ product.pretty_name }}</v-card-title>
      <v-card-text>
        <v-row>
          <v-col cols="4">
            <h3>Aliases</h3>
            <v-progress-linear v-if="loadingAliases" indeterminate></v-progress-linear>
            <v-list>
              <v-list-item v-for="alias in aliases">{{ alias.ocr_text }}</v-list-item>
            </v-list>
          </v-col>
          <v-col cols="4">
            <h3>Codes</h3>
            <v-progress-linear v-if="loadingCodes" indeterminate></v-progress-linear>
            <v-list>
              <v-list-item v-for="code in codes">{{ code.ocr_text }}</v-list-item>
            </v-list>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script setup lang="ts">
import {ref, computed} from "vue";
import {handleErrors} from "@/utils";

const props = defineProps(['product'])
const _showDialog = ref(false)
const showDialog = computed({
  get() {
    return _showDialog.value
  },
  set(value) {
    _showDialog.value = value
    if (value) {
      initialize()
    }
  }
})
const aliases = ref([])
const loadingAliases = ref(false)
const loadedAliases = ref(false)

const codes = ref([])
const loadingCodes = ref(false)
const loadedCodes = ref(false)

function initialize() {
  ensureAliasesLoaded()
  ensureCodesLoaded()
}

function ensureAliasesLoaded() {
  if (!loadedAliases.value && !loadingAliases.value) {
    loadingAliases.value = true
    fetch(
      `http://localhost:9000/api/product-aliases/?value=${props.product.id}`
    )
      .then(handleErrors)
      .then(response => response.json())
      .then(data => {
        console.log(data)
        aliases.value = data.results
        loadedAliases.value = true
        loadingAliases.value = false
      })
  }
}

function ensureCodesLoaded() {
  if (!loadedCodes.value && !loadingCodes.value) {
    loadingCodes.value = true
    fetch(
      `http://localhost:9000/api/product-codes/?value=${props.product.id}`
    )
      .then(handleErrors)
      .then(response => response.json())
      .then(data => {
        console.log(data)
        codes.value = data.results
        loadedCodes.value = true
        loadingCodes.value = false
      })
  }
}
</script>
