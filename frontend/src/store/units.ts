import {defineStore} from 'pinia'
import {handleErrors} from "@/utils";
import {ref} from "vue";

// You can name the return value of `defineStore()` anything you want,
// but it's best to use the name of the store and surround it with `use`
// and `Store` (e.g. `useUserStore`, `useCartStore`, `useProductStore`)
// the first argument is a unique id of the store across your application
export const useUnitsStore = defineStore('units', () => {
  const units = ref([])
  const initialized = ref(false)

  async function createUnit(name: string) {
    await fetch(
      "http://localhost:9000/api/units/",
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({name: name})
      }
    )
      .then(handleErrors)
      .then(response => response.json())
      .then(data => units.value.unshift(data))
  }

  fetch("http://localhost:9000/api/units/")
    .then(handleErrors)
    .then((response) => response.json())
    .then(data => units.value = data.results.map(unit => ({id: unit.id, name: unit.name})))
    .then(() => initialized.value = true)

  return {units, initialized, createUnit}
})
