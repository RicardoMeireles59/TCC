// EasyEnglish – background.js
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.local.set({ active: true });
});
