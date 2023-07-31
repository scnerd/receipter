import {defineStore} from "pinia";
import {computed, Ref, ref} from "vue";
import {Property} from "@babel/types";

export function handleErrors(response: Response) {
  if (!response.ok) {
    console.log(response)
    throw Error(response.statusText)
  }
  return response
}

export async function patchField(model: string, pk: number, field: string, value: any) {
  await fetch(
    `http://localhost:9000/api/${model}/${pk}/`,
    {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        [field]: value,
      }),
    }
  )
    .then(handleErrors)
}


export interface DBObjBase {
  id?: number
}

export interface ExistingDBObj<T extends DBObjBase> {
  id: number
  [Property in keyof
  T
  as

  Exclude<Property, 'id'>

  ]
  : Type[Property];
}

export interface NewDBObj<T extends DBObjBase> {
  [Property in keyof
  T
  as

  Exclude<Property, 'id'>

  ]
  : Type[Property];
}

export interface PartialDBObj<T extends DBObjBase> {
  id: number
  [Property in keyof
  T
  as

  Exclude<Property, 'id'>

  ]+
  ?: Type[Property];
}


interface ListResponse<T extends DBObjBase> {
  count: number
  next?: string
  previous?: string
  results: ExistingDBObj<T>[]
}

export function defineDRFStore<T extends DBObjBase>(api_endpoint: string) {
  return defineStore(api_endpoint, () => {
    const objects: Ref<Map<number, ExistingDBObj<T>>> = ref(new Map())
    const initialized: Ref<boolean> = ref(false)
    const apiUrl: string = `http://localhost:9000/api/${api_endpoint}/`

    async function loadPage(url: string = apiUrl) {
      let data: ListResponse<ExistingDBObj<T>> = await fetch(url)
        .then(handleErrors)
        .then((response) => response.json())
      data.results.forEach(v => objects.value.set(v.id, v))
      return data.next
    }

    async function loadAll() {
      initialized.value = false
      objects.value.clear()

      let nextPage = await loadPage()

      while (nextPage != null) {
        nextPage = await loadPage(nextPage)
      }
      initialized.value = true
    }

    async function create(obj: NewDBObj<T>) {
      let data = await fetch(
        apiUrl,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(obj)
        }
      )
        .then(handleErrors)
        .then(response => response.json())
      objects.value.set(data.id, data)
      return data
    }

    async function update(obj: PartialDBObj<T>) {
      let data = await fetch(
        `${apiUrl}${obj.id}/`,
        {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(obj)
        }
      )
        .then(handleErrors)
        .then(response => response.json())
        // .then((data: ListResponse<T>) => data.results.forEach(v => objects.value.set(v.id, v)))
      objects.value.set(obj.id, obj)
      return data
    }

    async function delete_(id: number) {
      await fetch(
        `${apiUrl}${id}/`,
        {
          method: 'DELETE',
        }
      )
      .then(handleErrors)
      objects.value.delete(id)
    }

    const objectList = computed(() => Array.from(objects.value.values()))

    loadAll()

    return {objects, objectList, initialized, create, update, delete_}
  })
}
