<template>
    <div class="form-group">
      <label :for="inputId">{{ label }}</label>
      <component
        :is="tag"
        :type="type"
        v-model="modelValue"
        :id="inputId"
        :class="inputClass"
        :required="required"
        :placeholder="placeholder"
        :options="options"
        :min="min"
        @change="handleChange"
      >
        <option
          v-if="tag === 'select'"
          v-for="option in options"
          :key="option.value"
          :value="option.value"
        >
          {{ option.name }}
        </option>
      </component>
      <span v-if="error" class="error">{{ error }}</span>
    </div>
  </template>
  
  <script>
  export default {
    name: "FormField",
    props: {
      label: {
        type: String,
        required: true
      },
      modelValue: {
        required: true
      },
      type: {
        type: String,
        default: "text"
      },
      tag: {
        type: String,
        default: "input"
      },
      inputId: {
        type: String,
        required: true
      },
      inputClass: {
        type: String,
        default: "input-field"
      },
      required: {
        type: Boolean,
        default: false
      },
      error: {
        type: String,
        default: null
      },
      placeholder: {
        type: String,
        default: ""
      },
      options: {
        type: Array,
        default: () => []
      },
      min: {
        type: Number,
        default: null
      }
    },
    methods: {
      handleChange(event) {
        this.$emit("update:modelValue", event.target.value);
      }
    }
  };
  </script>
  
  <style scoped>
  .form-group {
    margin-bottom: 15px;
  }
  .error {
    color: red;
  }
  </style>
  