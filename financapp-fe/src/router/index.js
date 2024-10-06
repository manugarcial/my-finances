import Vue from 'vue';
import Router from 'vue-router';
import ScriptResult from '../components/ScriptResult.vue';

Vue.use(Router);

export default new Router({
  routes: [
    {
      path: '../../../../financapp/investing.py',
      name: 'Script1',
      component: ScriptResult
    }
  ]
});
