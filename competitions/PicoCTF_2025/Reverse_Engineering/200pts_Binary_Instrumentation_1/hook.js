var sleep_hook = Module.findExportByName("kernel32.dll", "Sleep");
Interceptor.replace(sleep_hook, new NativeCallback(function(ms) {
    console.log("[+] Bypassed Sleep: " + ms + "ms → 0ms");
}, 'void', ['uint32']));