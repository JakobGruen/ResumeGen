// PDF Service as HTTP Server
const express = require("express");
const puppeteer = require("puppeteer");
const fs = require("fs").promises;
const path = require("path");

const app = express();
const PORT = process.env.PORT || 3000;

// Remove global JSON middleware to prevent Buffer serialization
// app.use(express.json());
app.use(express.text({ type: "text/html" }));

async function generatePDF(html, options = {}) {
  const browser = await puppeteer.launch({
    args: [
      "--no-sandbox",
      "--disable-setuid-sandbox",
      "--disable-dev-shm-usage",
      "--disable-gpu",
      "--disable-extensions",
      "--disable-background-timer-throttling",
      "--disable-backgrounding-occluded-windows",
      "--disable-renderer-backgrounding",
    ],
    headless: "new",
    executablePath: process.env.PUPPETEER_EXECUTABLE_PATH,
  });

  try {
    const page = await browser.newPage();
    await page.setContent(html, {
      waitUntil: "networkidle0",
      timeout: 60000,
    });

    const pdfBuffer = await page.pdf({
      format: options.format || "A4",
      printBackground: true,
      timeout: 60000,
      ...options,
    });

    return pdfBuffer;
  } finally {
    await browser.close();
  }
}

// Health check endpoint
app.get("/health", (req, res) => {
  res.json({ status: "healthy", service: "PDF Generator" });
});

// Generate PDF from HTML content
app.post("/generate-pdf", express.json(), async (req, res) => {
  try {
    const { html, options } = req.body;

    if (!html) {
      return res.status(400).json({ error: "HTML content is required" });
    }

    const pdfBuffer = await generatePDF(html, options);

    res.setHeader("Content-Type", "application/pdf");
    res.setHeader("Content-Disposition", 'attachment; filename="document.pdf"');
    res.end(pdfBuffer, "binary");
  } catch (error) {
    console.error("Error generating PDF:", error);
    res
      .status(500)
      .json({ error: "Failed to generate PDF", details: error.message });
  }
});

// Generate PDF from HTML file path
app.post("/generate-pdf-from-file", express.json(), async (req, res) => {
  try {
    const { filePath, options } = req.body;

    if (!filePath) {
      return res.status(400).json({ error: "File path is required" });
    }

    const html = await fs.readFile(filePath, "utf-8");
    const pdfBuffer = await generatePDF(html, options);

    res.setHeader("Content-Type", "application/pdf");
    res.setHeader(
      "Content-Disposition",
      `attachment; filename="${path.basename(filePath, ".html")}.pdf"`
    );
    res.end(pdfBuffer, "binary");
  } catch (error) {
    console.error("Error generating PDF from file:", error);
    res.status(500).json({
      error: "Failed to generate PDF from file",
      details: error.message,
    });
  }
});

app.listen(PORT, () => {
  console.log(`PDF Service running on port ${PORT}`);
});

// Export for module usage
module.exports = { generatePDF };
