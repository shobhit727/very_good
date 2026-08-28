// Ask the visitor for permission before collecting technical telemetry.
async function requestTelemetryConsent() {
  // Ask for explicit consent instead of silently collecting information.
  const consent = window.confirm(
    "Allow this page to collect basic technical information such as browser, " +
    "language, screen size, timezone, and referrer for analytics?"
  );

  // Stop immediately when the visitor declines.
  if (!consent) {
    return;
  }

  // Build the limited telemetry payload.
  const telemetry = {
    user_agent: navigator.userAgent,
    language: navigator.language,
    platform: navigator.platform,
    screen_width: window.screen.width,
    screen_height: window.screen.height,
    timezone: Intl.DateTimeFormat().resolvedOptions().timeZone,
    referrer: document.referrer
  };

  // Send the consented telemetry to the Python backend.
  await fetch("/api/visit", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(telemetry)
  });
}

// Run the consent request after the page has loaded.
window.addEventListener("load", requestTelemetryConsent);
