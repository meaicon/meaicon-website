(function () {
  var STORAGE_KEY = 'meaicon_cookie_consent_v1';
  var CONSENT_EVENT = 'meaicon:consent-updated';

  var defaultConsent = {
    necessary: true,
    analytics: false,
    marketing: false,
    decided: false,
    updatedAt: null
  };

  function readConsent() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (!raw) return Object.assign({}, defaultConsent);
      return Object.assign({}, defaultConsent, JSON.parse(raw));
    } catch (e) {
      return Object.assign({}, defaultConsent);
    }
  }

  function saveConsent(consent) {
    var next = Object.assign({}, defaultConsent, consent, { necessary: true, updatedAt: new Date().toISOString() });
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next));
    window.dispatchEvent(new CustomEvent(CONSENT_EVENT, { detail: next }));
    return next;
  }

  function hasConsent() {
    return readConsent().decided === true;
  }

  function applyGoogleConsentMode(consent) {
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { dataLayer.push(arguments); };
    gtag('consent', consent.decided ? 'update' : 'default', {
      analytics_storage: consent.analytics ? 'granted' : 'denied',
      ad_storage: 'denied',
      ad_user_data: 'denied',
      ad_personalization: 'denied',
      functionality_storage: 'granted',
      personalization_storage: 'denied',
      security_storage: 'granted',
      wait_for_update: 500
    });
  }

  function loadGA() {
    if (document.querySelector('script[data-meaicon-ga]')) return;
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=G-K2L9LYGJBV';
    s.setAttribute('data-meaicon-ga', 'true');
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function () { dataLayer.push(arguments); };
    gtag('js', new Date());
    gtag('config', 'G-K2L9LYGJBV', { anonymize_ip: true });
  }

  function syncTracking(consent) {
    applyGoogleConsentMode(consent);
    if (consent.analytics) loadGA();
  }

  /* --- Focus trap --- */
  var focusTrapHandler = null;

  function trapFocus(modal) {
    var focusable = modal.querySelectorAll('button, [href], input, [tabindex]:not([tabindex="-1"])');
    if (focusable.length === 0) return;
    var first = focusable[0];
    var last = focusable[focusable.length - 1];
    first.focus();
    focusTrapHandler = function (e) {
      if (e.key === 'Escape') {
        modal.classList.remove('is-open');
        untrapFocus();
        var trigger = document.querySelector('[data-open-cookie-settings]');
        if (trigger) trigger.focus();
        return;
      }
      if (e.key !== 'Tab') return;
      if (e.shiftKey) {
        if (document.activeElement === first) { e.preventDefault(); last.focus(); }
      } else {
        if (document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    };
    document.addEventListener('keydown', focusTrapHandler);
  }

  function untrapFocus() {
    if (focusTrapHandler) {
      document.removeEventListener('keydown', focusTrapHandler);
      focusTrapHandler = null;
    }
  }

  /* --- Banner --- */
  function createBanner() {
    if (hasConsent()) return;

    var banner = document.createElement('div');
    banner.id = 'cookie-consent-banner';
    banner.innerHTML =
      '<div class="cc-card" role="dialog" aria-live="polite" aria-label="Cookie consent">' +
        '<div class="cc-text">' +
          '<p>We use essential cookies for site security. Optional analytics cookies help us improve. ' +
          '<a href="/privacy-policy.html">Privacy Policy</a></p>' +
        '</div>' +
        '<div class="cc-actions">' +
          '<button type="button" class="cc-btn cc-btn-secondary" data-cc-action="reject">Reject</button>' +
          '<button type="button" class="cc-btn cc-btn-link" data-cc-action="customize">Customize</button>' +
          '<button type="button" class="cc-btn cc-btn-primary" data-cc-action="accept">Accept</button>' +
        '</div>' +
      '</div>';
    document.body.appendChild(banner);

    banner.addEventListener('click', function (e) {
      var action = e.target && e.target.getAttribute && e.target.getAttribute('data-cc-action');
      if (!action) return;

      if (action === 'accept') {
        var consent = saveConsent({ decided: true, analytics: true, marketing: false });
        syncTracking(consent);
        banner.remove();
      }
      if (action === 'reject') {
        var consent2 = saveConsent({ decided: true, analytics: false, marketing: false });
        syncTracking(consent2);
        banner.remove();
      }
      if (action === 'customize') {
        openPreferences();
      }
    });
  }

  /* --- Preferences modal --- */
  function openPreferences() {
    var modal = document.getElementById('cookie-preferences-modal');
    var current = readConsent();

    if (!modal) {
      modal = document.createElement('div');
      modal.id = 'cookie-preferences-modal';
      modal.innerHTML =
        '<div class="cc-modal-backdrop" data-cc-close="true"></div>' +
        '<div class="cc-modal" role="dialog" aria-modal="true" aria-label="Cookie preferences">' +
          '<h3>Cookie preferences</h3>' +
          '<p>Manage which cookies you allow. Necessary cookies are always active.</p>' +
          '<label class="cc-toggle">' +
            '<input type="checkbox" checked disabled>' +
            '<span>Necessary (always active)</span>' +
          '</label>' +
          '<label class="cc-toggle">' +
            '<input id="cc-analytics" type="checkbox">' +
            '<span>Analytics (help us improve)</span>' +
          '</label>' +
          '<div class="cc-actions" style="margin-top:16px">' +
            '<button type="button" class="cc-btn cc-btn-secondary" data-cc-save="reject">Reject all</button>' +
            '<button type="button" class="cc-btn cc-btn-primary" data-cc-save="save">Save</button>' +
          '</div>' +
        '</div>';
      document.body.appendChild(modal);

      modal.addEventListener('click', function (e) {
        if (e.target.matches && e.target.matches('[data-cc-close="true"]')) {
          modal.classList.remove('is-open');
          untrapFocus();
          return;
        }
        var saveAction = e.target && e.target.getAttribute && e.target.getAttribute('data-cc-save');
        if (!saveAction) return;

        if (saveAction === 'reject') {
          var consent = saveConsent({ decided: true, analytics: false, marketing: false });
          syncTracking(consent);
          modal.classList.remove('is-open');
          untrapFocus();
          var banner = document.getElementById('cookie-consent-banner');
          if (banner) banner.remove();
        }
        if (saveAction === 'save') {
          var analytics = modal.querySelector('#cc-analytics').checked;
          var consent2 = saveConsent({ decided: true, analytics: analytics, marketing: false });
          syncTracking(consent2);
          modal.classList.remove('is-open');
          untrapFocus();
          var banner2 = document.getElementById('cookie-consent-banner');
          if (banner2) banner2.remove();
        }
      });
    }

    modal.querySelector('#cc-analytics').checked = !!current.analytics;
    modal.classList.add('is-open');
    trapFocus(modal.querySelector('.cc-modal'));
  }

  /* --- Settings triggers (footer link etc.) --- */
  function attachSettingsTriggers() {
    document.addEventListener('click', function (e) {
      var trigger = e.target.closest && e.target.closest('[data-open-cookie-settings]');
      if (!trigger) return;
      e.preventDefault();
      openPreferences();
    });
  }

  /* --- Init --- */
  var consent = readConsent();
  applyGoogleConsentMode(consent);

  document.addEventListener('DOMContentLoaded', function () {
    createBanner();
    attachSettingsTriggers();
    if (consent.decided && consent.analytics) {
      loadGA();
    }
  });
})();
