
let scripts = [
  ["handle.js"]
];

scripts.forEach(s => {
  let script = document.createElement('script');
  script.src = chrome.runtime.getURL(s[0]);

  (document.head||document.documentElement).prepend(script);
});





// chrome.runtime.sendMessage({message:"deleteAll!"});







