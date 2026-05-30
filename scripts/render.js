const vega = require('vega');
const vegaLite = require('vega-lite');
const fs = require('fs');

const spec = JSON.parse(fs.readFileSync('vega-lite/chart4_choropleth_map.json', 'utf8'));
const compiled = vegaLite.compile(spec).spec;
const view = new vega.View(vega.parse(compiled), {renderer: 'none'});

view.toSVG().then(function(svg) {
  fs.writeFileSync('test.svg', svg);
  console.log("SVG rendered");
}).catch(function(err) { console.error(err); });
