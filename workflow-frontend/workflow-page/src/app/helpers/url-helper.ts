const PROJECT_KEY = 'projectId';

export const UrlHelper = {
  getProjectId(): string | null {
    const parameters = new URLSearchParams(window.location.search);
    return parameters.get(PROJECT_KEY);
  },

  updateParameter(projectId: string) {
    const parameters = new URLSearchParams(window.location.search);
    if (projectId == null) {
      parameters.delete(PROJECT_KEY);
    } else {
      parameters.set(PROJECT_KEY, projectId);
    }
    return parameters.toString();
  },
};
