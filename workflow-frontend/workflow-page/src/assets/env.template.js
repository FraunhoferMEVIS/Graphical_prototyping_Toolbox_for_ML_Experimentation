(function (window) {
  window["env"] = window["env"] || {};

  // Environment variables
  window["env"]["maratusBasePathFrontend"] = "${MARATUS_BASE_PATH}" || "";
  window["env"]["mlkitchenBasePathFrontEnd"] = "${MLKITCHEN_BASE_PATH}" || "";
  window["env"]["mlflowBasePath"] = "${MLFLOW_BASE_PATH}" || "";
  window["env"]["projectManagerBasePath"] =
    "${PROJECT_MANAGER_BASE_PATH}" || "";
})(this);
