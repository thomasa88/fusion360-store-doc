// ==UserScript==
// @name Autodesk store - bigger fields
// @namespace Violentmonkey Scripts
// @match https://apps.autodesk.com/en/Publisher/SubmitProduct?*
// @grant GM_addStyle
// ==/UserScript==

GM_addStyle ( `
    iframe {
        height: 400px !important;
    }
` );
