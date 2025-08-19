import { OverlayContainer } from '@angular/cdk/overlay';
import { Component } from '@angular/core';
import Cookies from 'js-cookie';

const THEME_KEY = 'theme-preference';
const DETECTION_INTERVAL = 2000;

type Theme = 'dark' | 'light' | 'sys';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent {
  title = 'data-preparation';
  isDark: boolean = false;
  mediaQuery: MediaQueryList;

  // keep track of last read theme value
  // to periodically detect changes
  previousTheme: Theme | undefined;

  constructor(private overlayContainer: OverlayContainer) {
    this.mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    this.mediaQuery.addEventListener('change', (event) => {
      const theme = this.readThemePreference();
      if (theme === null || theme == 'sys') {
        // only react if user prefers sys settings
        this.applyLightDarkTheme(event.matches ? 'dark' : 'light');
      }
    });
  }

  ngOnInit() {
    this.loadThemePreference();
    this.observeCookieChange();
  }

  /**
   * Load theme cookie and apply theme.
   */
  private loadThemePreference() {
    const savedTheme = this.readThemePreference();
    this.previousTheme = savedTheme;

    this.applyTheme(savedTheme);
  }

  /**
   * Periodically check if workflow page changed cookie value.
   */
  private observeCookieChange() {
    setInterval(() => {
      const theme = this.readThemePreference();
      if (theme != this.previousTheme) {
        this.applyTheme(theme);
        this.previousTheme = theme;
      }
    }, DETECTION_INTERVAL);
  }

  private applyTheme(theme: Theme) {
    if (theme == null) {
      this.applyOsTheme();
    } else if (theme == 'sys') {
      this.applyOsTheme();
    } else {
      this.applyLightDarkTheme(theme);
    }
  }

  private applyOsTheme() {
    this.applyLightDarkTheme(this.mediaQuery.matches ? 'dark' : 'light');
  }

  /**
   * Sets or removes dark-theme css class.
   */
  private applyLightDarkTheme(theme: Theme) {
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
   * Read theme preference from cookie.
   */
  private readThemePreference() {
    return Cookies.get(THEME_KEY) as Theme;
  }
}
