// Génère le PDF A4 : node build.js
const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch();const p=await b.newPage();
p.on('pageerror',e=>console.log('ERR',e.message));
await p.goto('file://'+__dirname+'/devis.html');await p.evaluate(()=>document.fonts.ready);
console.log(JSON.stringify(await p.evaluate(()=>window.TOTAUX)));
await p.pdf({path:__dirname+'/Estimation_Maison_Modulaire_60m2_BravosHabitat.pdf',format:'A4',printBackground:true,preferCSSPageSize:true});
await b.close()})();
