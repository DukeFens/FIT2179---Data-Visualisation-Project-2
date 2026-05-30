const vega = require('vega');
const vegaLite = require('vega-lite');
const fs = require('fs');
const path = require('path');
const PROJ = path.resolve(__dirname, '..');
const specs = process.argv.slice(2);
(async () => {
  for (const s of specs) {
    const file = path.join(PROJ, 'vega-lite', s + '.json');
    if (!fs.existsSync(file)) { console.log(`\n[${s}] ❌ FILE MISSING: ${file}`); continue; }
    let spec;
    try { spec = JSON.parse(fs.readFileSync(file,'utf8')); }
    catch(e){ console.log(`\n[${s}] ❌ JSON PARSE: ${e.message}`); continue; }
    let compiled;
    try { compiled = vegaLite.compile(spec).spec; }
    catch(e){ console.log(`\n[${s}] ❌ VL COMPILE: ${e.message}`); continue; }
    try {
      const loader = vega.loader({ baseURL: PROJ + '/' });
      const view = new vega.View(vega.parse(compiled), { loader, renderer:'none' });
      const warns = [];
      view.warn = (...a)=>warns.push(a.join(' '));
      await view.runAsync();
      await view.toSVG();
      console.log(`\n[${s}] ✅ OK${warns.length? '  ⚠ '+warns.length+' warns: '+warns.slice(0,2).join(' | '):''}`);
    } catch(e){ console.log(`\n[${s}] ❌ RUNTIME: ${e.message}`); }
  }
})();
