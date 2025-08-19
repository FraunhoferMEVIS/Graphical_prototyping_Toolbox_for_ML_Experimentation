(function (window) {
  window["env"] = window["env"] || {};

  // Environment variables
  window["env"]["backendBasePath"] = "${BACKEND_BASE_PATH}" || "";
  window["env"]["projectManagerBasePath"] =
    "${PROJECT_MANAGER_BASE_PATH}" || "";
  window["env"]["dataDescriptorBasePath"] =
    "${DATA_DESCRIPTOR_BASE_PATH}" || "";
  window["env"]["workflowPageBasePath"] = "${WORKFLOW_PAGE_BASE_PATH}" || "";
})(this);
