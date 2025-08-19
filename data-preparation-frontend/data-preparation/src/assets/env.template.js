(function (window) {
  window['env'] = window['env'] || {};

  // Environment variables
  window['env']['projectManagerBasePath'] =
    '${PROJECT_MANAGER_BASE_PATH}' || '';
  window['env']['dataPreparationBasePath'] =
    '${DATA_PREPARATION_BASE_PATH}' || '';
  window['env']['workflowPageBasePath'] = '${WORKFLOW_PAGE_BASE_PATH}' || '';
})(this);
