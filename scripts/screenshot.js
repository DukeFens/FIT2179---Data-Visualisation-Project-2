const puppeteer = require('puppeteer');
(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.setViewport({ width: 1000, height: 800 });
  await page.goto('http://localhost:8000/test.html', { waitUntil: 'networkidle0' });
  await page.screenshot({ path: '/Users/dukephan/.gemini/antigravity/brain/b1796860-3505-4b90-ac5c-1b68a1f6ceb2/scratch/chart4_test.png' });
  await browser.close();
})();
