import { Component } from '@angular/core';
import { OverlayContainer } from '@angular/cdk/overlay';
import Cookies from 'js-cookie';

const THEME_KEY = 'theme-preference';
export type Theme = 'dark' | 'light' | 'sys';

@Component({
  selector: 'app-workflow-home',
  templateUrl: './workflow-home.component.html',
  styleUrls: ['./workflow-home.component.css'],
})
export class WorkflowHomeComponent {
  isDark: boolean = false;
  mediaQuery: MediaQueryList;

  constructor(private overlayContainer: OverlayContainer) {
    this.mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    this.mediaQuery.addEventListener('change', (event) => {
      const theme = this.readThemePreference();
      if (theme === null || theme == 'sys') {
        // only react if user prefers sys settings
        this.applyTheme(event.matches ? 'dark' : 'light');
      }
    });
  }

  ngOnInit() {
    this.loadThemePreference();
  }

  /**
   * Persists user choice and applies selected theme.
   */
  onThemeSelected(theme: Theme) {
    this.setThemePreference(theme);
    if (theme == 'sys') {
      this.applyOsTheme();
    } else {
      this.applyTheme(theme);
    }
  }

  private applyOsTheme() {
    this.applyTheme(this.mediaQuery.matches ? 'dark' : 'light');
  }

  /**
   * Applies theme to UI.
   */
  private applyTheme(theme: Theme) {
    if (theme == 'dark') {
      this.isDark = true;

      this.overlayContainer.getContainerElement().classList.add('dark-theme');
    } else {
      this.isDark = false;

      this.overlayContainer
        .getContainerElement()
        .classList.remove('dark-theme');
    }
  }

  /**
   * Load theme cookie and apply theme.
   */
  private loadThemePreference() {
    const savedTheme = this.readThemePreference();
    if (savedTheme == null) {
      this.applyOsTheme();
    } else if (savedTheme == 'sys') {
      this.applyOsTheme();
    } else {
      this.applyTheme(savedTheme);
    }
  }

  /**
   * Read theme preference from cookie.
   */
  private readThemePreference() {
    return Cookies.get(THEME_KEY) as Theme;
  }

  /**
   * Persists selected theme as cookie.
   */
  private setThemePreference(theme: Theme) {
    Cookies.set(THEME_KEY, theme.toString(), {
      domain: this.getParentDomain(),
      path: '/',
    });
  }

  getParentDomain() {
    var hostName = location.hostname;
    if (hostName === 'localhost') {
      return null;
    } else {
      var domainParts = hostName.split('.');
      domainParts.shift();
      var parentDomain = domainParts.join('.');
      return parentDomain;
    }
  }
}
