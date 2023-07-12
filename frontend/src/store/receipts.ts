import {defineStore} from 'pinia'
import {handleErrors} from "@/utils";
import {ref} from "vue";

// You can name the return value of `defineStore()` anything you want,
// but it's best to use the name of the store and surround it with `use`
// and `Store` (e.g. `useUserStore`, `useCartStore`, `useProductStore`)
// the first argument is a unique id of the store across your application
export const useReceiptsStore = defineStore('receipts', () => {
  const receipts = ref([])
  const initialized = ref(false)

  fetch("http://localhost:8000/api/receipts/")
    .then(handleErrors)
    .then((response) => response.json())
    .then(data => receipts.value = data.results)
    .then(() => initialized.value = true)

  return {receipts, initialized}
})
