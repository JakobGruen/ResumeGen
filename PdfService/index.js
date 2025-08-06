// This file is the entry point for the Node.js package. It contains the logic for generating PDFs using Puppeteer.

const puppeteer = require("puppeteer");

async function generatePDF(htmlPath, pdfPath) {
  const browser = await puppeteer.launch({
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--disable-dev-shm-usage",
      "--disable-gpu",
    ],
    headless: true,
    executablePath: process.env.PUPPETEER_EXECUTABLE_PATH,
  });
  const page = await browser.newPage();
  await page.goto("file://" + htmlPath, {
    waitUntil: "networkidle0",
    timeout: 60000,
  });
  await page.pdf({
    path: pdfPath,
    format: "A4",
    printBackground: true,
    timeout: 60000,
  });
  await browser.close();
}

module.exports = { generatePDF };

// CLI usage
if (require.main === module) {
  const [, , htmlPath, pdfPath] = process.argv;
  if (!htmlPath || !pdfPath) {
    console.error("Usage: node index.js <input.html> <output.pdf>");
    process.exit(1);
  }

  generatePDF(htmlPath, pdfPath)
    .then(() => console.log("PDF generated:", pdfPath))
    .catch((err) => {
      console.error("Error generating PDF:", err);
      process.exit(1);
    });
}
