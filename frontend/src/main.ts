// This is a TypeScript file that will be compiled to JavaScript
// For now, we'll create a JavaScript version that can be used directly

const { createApp, ref } = Vue;

const App = {
  setup() {
    const question = ref('');
    const language = ref('zh');
    const answer = ref('');
    const evidence = ref([]);
    const graphHits = ref([]);
    const loading = ref(false);
    const error = ref('');

    const getAnswer = async () => {
      if (!question.value.trim()) {
        error.value = 'Please enter a question';
        return;
      }

      loading.value = true;
      error.value = '';
      answer.value = '';
      evidence.value = [];
      graphHits.value = [];

      try {
        const response = await axios.post('http://127.0.0.1:8000/qa/rag', {
          question: question.value,
          lang: language.value
        });

        answer.value = response.data.answer;
        evidence.value = response.data.evidence;
        graphHits.value = response.data.graph_hits;
      } catch (err) {
        console.error('Error getting answer:', err);
        if (err.response) {
          error.value = `Error: ${err.response.data.detail || 'Failed to get answer'}`;
        } else if (err.request) {
          error.value = 'Network error: Could not connect to the API. Please make sure the backend is running.';
        } else {
          error.value = `Error: ${err.message}`;
        }
      } finally {
        loading.value = false;
      }
    };

    return {
      question,
      language,
      answer,
      evidence,
      graphHits,
      loading,
      error,
      getAnswer
    };
  }
};

// Mount the app
createApp(App).mount('#app');