export const UrlHelper = {

    getProjectId(): string | null {
        const key = "projectId";
        const parameters = new URLSearchParams(window.location.search);
        let value = parameters.get(key);
        
        // TODO: remove fallback project id once we know how standalone mode works
        return value ?? "test"
    }
}