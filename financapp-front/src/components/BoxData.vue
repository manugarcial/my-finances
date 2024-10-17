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
      number: this.initialNumber,
      text: this.initialText,
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

<style scoped></style>
