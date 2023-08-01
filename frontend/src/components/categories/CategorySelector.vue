<template>
  <Selector
    :id="category"
    :store="categoryStore"
    :allow-clear="true"
    :allow-delete="true"
    :parent-store="parentStore"
    :parent-id="parentId"
    :parent-attr="parentAttr"
    title-attr="name"
    label="Category"
    >
    <template v-slot:create="s"><CategoryCreator @create:category="v => category = v"></CategoryCreator></template>
    <template v-slot:edit="s"><CategoryEditor :category="s.object"></CategoryEditor></template>
  </Selector>
</template>

<script setup lang="ts">
import {useCategoryStore} from "@/store/app";
import {computed, ref} from "vue";
import CategoryCreator from "@/components/categories/CategoryCreator.vue";
import Selector from "@/components/generic/Selector.vue";
import CategoryEditor from "@/components/categories/CategoryEditor.vue";

const props = defineProps<{
  id?: number
  parentStore?: any
  parentId?: number
  parentAttr?: string
}>()

const emit = defineEmits(["update:modelValue"])

const categoryStore = useCategoryStore()

const category = computed({
  get() {
    return props.id ?? props.parentStore.objects.get(props.parentId)[props.parentAttr]
  },
  set(e) {
    emit('update:modelValue', e);
  }
})
</script>
