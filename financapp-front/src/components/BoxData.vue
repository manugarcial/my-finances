<template>
  <div class="box-data-container">
    <h2>{{ text }}</h2>
    <div class="output">
      <p><strong>Value:</strong> {{ number }}</p>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    initialNumber: {
      type: Number,
      required: true,
    },
    initialText: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      number: this.initialNumber, // Initialize with the prop value
      text: this.initialText, // Initialize with the prop value
    };
  },
  watch: {
    initialNumber(newVal) {
      this.number = newVal;
    },
    initialText(newVal) {
      this.text = newVal;
    },
  },
};
</script>

<style scoped>
/* .box-data-container {
  max-width: 500px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.input-field {
  margin-bottom: 15px;
}

.input-field label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.input-field input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.output {
  margin-top: 20px;
  border-top: 1px solid #ddd;
  padding-top: 10px;
}

.output h3 {
  margin-bottom: 10px;
} */
</style>
