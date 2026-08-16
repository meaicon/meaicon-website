(function () {
  const STORAGE_KEY = 'meaicon_cookie_consent_v1';
  const CONSENT_EVENT = 'meaicon:consent-updated';

  const defaultConsent = {
    necessary: true,
    analytics: false,
    marketing: false,
    decided: false,
    updatedAt: null
  };

  function readConsent() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return { ...defaultConsent };
      return { ...defaultConsent, ...JSON.parse(raw) };
    } catch {
      return { ...defaultConsent };
    }
  }

  function saveConsent(consent) {
    const next = {
      ...defaultConsent,
      ...consent,
      necessary: true,
      updatedAt: new Date().toISOString()
    };
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    window.dispatchEvent(new CustomEvent(CONSENT_EVENT, { detail: next }));
    return next;
  }

  function hasConsent() {
    return readConsent().decided === true;
  }

  function applyGoogleConsentMode(consent) {
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function(){ dataLayer.push(arguments); };

    gtag('consent', consent.decided ? 'update' : 'default', {
      analytics_storage: consent.analytics ? 'granted' : 'denied',
      ad_storage: consent.marketing ? 'granted' : 'denied',
      ad_user_data: consent.marketing ? 'granted' : 'denied',
      ad_personalization: consent.marketing ? 'granted' : 'denied',
      functionality_storage: 'granted',
      personalization_storage: 'denied',
      security_storage: 'granted',
      wait_for_update: 500
    });
  }

  function loadGA() {
    if (document.querySelector('script[data-meaicon-ga]')) return;
    const s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=G-K2L9LYGJBV';
    s.setAttribute('data-meaicon-ga', 'true');
    document.head.appendChild(s);

    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function(){ dataLayer.push(arguments); };
    gtag('js', new Date());
    gtag('config', 'G-K2L9LYGJBV');
  }

  function syncTracking(consent) {
    applyGoogleConsentMode(consent);
    if (consent.analytics) loadGA();
  }

  function createBanner() {
    if (hasConsent()) return;

    const banner = document.createElement('div');
    banner.id = 'cookie-consent-banner';
    banner.innerHTML = `
      <div class="cc-card" role="dialog" aria-live="polite" aria-label="Cookie preferences">
        <div class="cc-text">
          <span class="cc-kicker">Privacy & cookies</span>
          <h3>Your privacy and website preferences.</h3>
          <p>This website uses strictly necessary cookies to provide secure, reliable access and analytics cookies to understand how visitors use our services. You may accept all, reject non-essential cookies, or customize your settings at any time.</p>
          <p class="mt-2"><a href="/privacy-policy.html">Review our Privacy Policy</a></p>
        </div>
        <div class="cc-actions">
          <button type="button" class="cc-btn cc-btn-secondary" data-cc-action="reject">Reject non-essential</button>
          <button type="button" class="cc-btn cc-btn-secondary" data-cc-action="customize">Customize</button>
          <button type="button" class="cc-btn cc-btn-primary" data-cc-action="accept">Accept all</button>
        </div>
      </div>
    `;
    document.body.appendChild(banner);

    banner.addEventListener('click', function (e) {
      const action = e.target && e.target.getAttribute('data-cc-action');
      if (!action) return;

      if (action === 'accept') {
        const consent = saveConsent({ decided: true, analytics: true, marketing: false });
        syncTracking(consent);
        banner.remove();
      }

      if (action === 'reject') {
        const consent = saveConsent({ decided: true, analytics: false, marketing: false });
        syncTracking(consent);
        banner.remove();
      }

      if (action === 'customize') {
        openPreferences();
      }
    });
  }

  function openPreferences() {
    let modal = document.getElementById('cookie-preferences-modal');
    const current = readConsent();

    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'cookie-preferences-modal';
      modal.innerHTML = `
        <div class="cc-modal-backdrop" data-cc-close="true"></div>
        <div class="cc-modal" role="dialog" aria-modal="true" aria-label="Cookie preferences">
          <h3>Manage cookie preferences</h3>
          <p>Necessary cookies are required for secure site operation and are always active. Analytics cookies help us measure visitor activity and improve our services. Marketing cookies remain disabled by default.</p>

          <label class="cc-toggle">
            <input type="checkbox" checked disabled>
            <span>Strictly necessary cookies (always active)</span>
          </label>

          <label class="cc-toggle">
            <input id="cc-analytics" type="checkbox">
            <span>Analytics cookies</span>
          </label>

          <label class="cc-toggle">
            <input id="cc-marketing" type="checkbox" disabled>
            <span>Marketing cookies (not active yet)</span>
          </label>

          <div class="cc-actions">
            <button type="button" class="cc-btn cc-btn-secondary" data-cc-save="reject">Reject non-essential</button>
            <button type="button" class="cc-btn cc-btn-primary" data-cc-save="save">Save preferences</button>
          </div>
        </div>
      `;
      document.body.appendChild(modal);

      modal.addEventListener('click', function (e) {
        if (e.target.matches('[data-cc-close="true"]')) {
          modal.classList.remove('is-open');
        }

        const saveAction = e.target && e.target.getAttribute('data-cc-save');
        if (!saveAction) return;

        if (saveAction === 'reject') {
          const consent = saveConsent({ decided: true, analytics: false, marketing: false });
          syncTracking(consent);
          modal.classList.remove('is-open');
          document.getElementById('cookie-consent-banner')?.remove();
        }

        if (saveAction === 'save') {
          const analytics = modal.querySelector('#cc-analytics').checked;
          const consent = saveConsent({ decided: true, analytics, marketing: false });
          syncTracking(consent);
          modal.classList.remove('is-open');
          document.getElementById('cookie-consent-banner')?.remove();
        }
      });
    }

    modal.querySelector('#cc-analytics').checked = !!current.analytics;
    modal.classList.add('is-open');
  }

  function attachSettingsTriggers() {
    document.addEventListener('click', function (e) {
      const trigger = e.target.closest('[data-open-cookie-settings]');
      if (!trigger) return;
      e.preventDefault();
      openPreferences();
    });
  }

  const consent = readConsent();
  applyGoogleConsentMode(consent);

  document.addEventListener('DOMContentLoaded', function () {
    createBanner();
    attachSettingsTriggers();
    if (consent.decided && consent.analytics) {
      loadGA();
    }
  });
})();
