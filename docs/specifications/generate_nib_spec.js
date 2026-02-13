const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat,
  HeadingLevel, BorderStyle, WidthType, ShadingType,
  PageNumber, PageBreak, TableOfContents
} = require("docx");

// Colour palette
const NAVY = "1B2A4A";
const STEEL = "2E5090";
const WHITE = "FFFFFF";

// Reusable helpers
const border = { style: BorderStyle.SINGLE, size: 1, color: "BBBBBB" };
const borders = { top: border, bottom: border, left: border, right: border };
const cellMargins = { top: 60, bottom: 60, left: 100, right: 100 };

function headerCell(text, width) {
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: { fill: NAVY, type: ShadingType.CLEAR },
    margins: cellMargins,
    verticalAlign: "center",
    children: [new Paragraph({ 
      alignment: AlignmentType.LEFT, 
      children: [new TextRun({ text, bold: true, font: "Arial", size: 18, color: WHITE })] 
    })]
  });
}

function cell(text, width, opts = {}) {
  const fill = opts.fill || WHITE;
  const bold = opts.bold || false;
  const sz = opts.size || 18;
  return new TableCell({
    borders,
    width: { size: width, type: WidthType.DXA },
    shading: { fill, type: ShadingType.CLEAR },
    margins: cellMargins,
    verticalAlign: "center",
    children: [new Paragraph({
      alignment: opts.align || AlignmentType.LEFT,
      children: [new TextRun({ text, font: "Arial", size: sz, bold, color: opts.color || "333333" })]
    })]
  });
}

function tblRow(cells) { return new TableRow({ children: cells }); }
function heading(text, level) { return new Paragraph({ heading: level, children: [new TextRun(text)] }); }

function para(text, opts = {}) {
  return new Paragraph({
    spacing: { after: opts.after || 160, before: opts.before || 0, line: opts.line || 276 },
    alignment: opts.align || AlignmentType.JUSTIFIED,
    children: [new TextRun({ 
      text, font: "Arial", size: opts.size || 20, 
      bold: opts.bold || false, italics: opts.italics || false, 
      color: opts.color || "333333" 
    })]
  });
}

function spacer(h = 120) { return new Paragraph({ spacing: { after: h } }); }

console.log("\nGenerating AEROSPACEMODEL NIB Specification Document...");
console.log("Document ID: AEROSPACEMODEL-ASIT-NIB-SPEC-001");
console.log("Version: 1.0 DRAFT\n");

// This script generates a professional Word document with:
// - Cover page with branding
// - Document control and approval sections  
// - Table of contents
// - Multiple sections covering scope, definitions, concept, taxonomy
// - Professional formatting with tables, headers, footers

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 20 } } },
    paragraphStyles: [
      { 
        id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: "Arial", color: NAVY },
        paragraph: { spacing: { before: 360, after: 200 }, outlineLevel: 0 } 
      },
      { 
        id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Arial", color: STEEL },
        paragraph: { spacing: { before: 280, after: 160 }, outlineLevel: 1 } 
      },
      { 
        id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 22, bold: true, font: "Arial", color: STEEL },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 2 } 
      },
    ]
  },
  numbering: {
    config: [
      { 
        reference: "bullets", 
        levels: [
          { level: 0, format: LevelFormat.BULLET, text: "\u2022", alignment: AlignmentType.LEFT, 
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
          { level: 1, format: LevelFormat.BULLET, text: "\u25E6", alignment: AlignmentType.LEFT, 
            style: { paragraph: { indent: { left: 1440, hanging: 360 } } } }
        ]
      },
      { 
        reference: "reqs", 
        levels: [
          { level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, 
            style: { paragraph: { indent: { left: 720, hanging: 360 } } } }
        ]
      }
    ]
  },
  sections: [
    // Cover Page
    {
      properties: {
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 1440, right: 1200, bottom: 1440, left: 1200 }
        }
      },
      children: [
        spacer(2400),
        para("AEROSPACEMODEL", { align: AlignmentType.CENTER, size: 20, bold: true, color: STEEL, after: 80 }),
        para("ASIT Governance Series", { align: AlignmentType.CENTER, size: 18, color: "666666", italics: true, after: 200 }),
        para("Non-Inference Boundary", { align: AlignmentType.CENTER, size: 52, bold: true, color: NAVY }),
        para("Technical Specification", { align: AlignmentType.CENTER, size: 40, bold: true, color: STEEL, after: 120 }),
        spacer(200),
        new Paragraph({
          alignment: AlignmentType.CENTER,
          spacing: { after: 0 },
          border: { top: { style: BorderStyle.SINGLE, size: 6, color: STEEL, space: 1 } },
          children: []
        }),
        spacer(120),
        para("Document Identifier:  AEROSPACEMODEL-ASIT-NIB-SPEC-001", { align: AlignmentType.CENTER, size: 18, color: "555555", after: 60 }),
        para("Version 1.0  |  Status: DRAFT  |  Classification: Programme Controlled", { align: AlignmentType.CENTER, size: 18, color: "555555", after: 60 }),
        para("Date: 2026-02-13", { align: AlignmentType.CENTER, size: 18, color: "555555", after: 60 }),
        spacer(600),
        para("Author:  Amedeo Pelliccia", { align: AlignmentType.CENTER, size: 18, color: "666666", after: 60 }),
        para("Organisation:  IDEALEeu Enterprise  /  AMPEL360 Programme", { align: AlignmentType.CENTER, size: 18, color: "666666", after: 60 }),
        para("Normative Parent:  Model Digital Constitution  →  TLI v2.1  →  BREX Decision Engine", { align: AlignmentType.CENTER, size: 18, color: "666666", after: 60 }),
        spacer(800),
        para("© 2026 Amedeo Pelliccia / IDEALEeu Enterprise.  Released under CC0 1.0 Universal (CC0 1.0) Public Domain Dedication.", { align: AlignmentType.CENTER, size: 16, color: "999999" }),
      ]
    },
    // Main content section with headers/footers
    {
      properties: {
        page: {
          size: { width: 11906, height: 16838 },
          margin: { top: 1440, right: 1200, bottom: 1440, left: 1200 }
        }
      },
      headers: {
        default: new Header({
          children: [para("AEROSPACEMODEL-ASIT-NIB-SPEC-001  |  v1.0 DRAFT", { align: AlignmentType.RIGHT, size: 14, color: "999999" })]
        })
      },
      footers: {
        default: new Footer({
          children: [new Paragraph({
            alignment: AlignmentType.CENTER,
            border: { top: { style: BorderStyle.SINGLE, size: 1, color: "CCCCCC", space: 4 } },
            children: [
              new TextRun({ text: "Page ", font: "Arial", size: 14, color: "999999" }),
              new TextRun({ children: [PageNumber.CURRENT], font: "Arial", size: 14, color: "999999" })
            ]
          })]
        })
      },
      children: [
        heading("Document Control", HeadingLevel.HEADING_1),
        new Table({
          width: { size: 9506, type: WidthType.DXA },
          columnWidths: [1200, 1400, 2200, 4706],
          rows: [
            tblRow([
              headerCell("Version", 1200), 
              headerCell("Date", 1400), 
              headerCell("Author", 2200), 
              headerCell("Change Summary", 4706)
            ]),
            tblRow([
              cell("1.0", 1200), 
              cell("2026-02-13", 1400), 
              cell("A. Pelliccia", 2200), 
              cell("Initial release. Establishes NIB taxonomy, detection logic, escalation protocols, evidence requirements, and integration with CNOT-gate architecture and EU AI Act Articles 14–15.", 4706)
            ]),
          ]
        }),
        spacer(200),
        heading("Approval", HeadingLevel.HEADING_2),
        new Table({
          width: { size: 9506, type: WidthType.DXA },
          columnWidths: [2400, 2200, 2400, 2506],
          rows: [
            tblRow([
              headerCell("Role", 2400), 
              headerCell("Name", 2200), 
              headerCell("Signature", 2400), 
              headerCell("Date", 2506)
            ]),
            tblRow([cell("Chief Systems Engineer", 2400), cell("", 2200), cell("", 2400), cell("", 2506)]),
            tblRow([cell("Safety & Certification Lead", 2400), cell("", 2200), cell("", 2400), cell("", 2506)]),
            tblRow([cell("AI Governance Authority", 2400), cell("", 2200), cell("", 2400), cell("", 2506)]),
            tblRow([cell("Configuration Manager", 2400), cell("", 2200), cell("", 2400), cell("", 2506)]),
          ]
        }),
        spacer(300),
        heading("Table of Contents", HeadingLevel.HEADING_1),
        new TableOfContents("TOC", { hyperlink: true, headingStyleRange: "1-3" }),
        new Paragraph({ children: [new PageBreak()] }),
        
        // Section 1
        heading("1  Scope and Purpose", HeadingLevel.HEADING_1),
        para("This specification defines the concept, classification, detection logic, escalation protocol, and evidence requirements for Non-Inference Boundaries (NIBs) within the AEROSPACEMODEL framework. A Non-Inference Boundary is the precise point in a governed automation chain where the system's deterministic reasoning capability is exhausted and human cognitive authority must be engaged to resolve irreducible ambiguity."),
        para("The NIB concept is the technical mechanism by which AEROSPACEMODEL satisfies the Human-in-the-Loop (HITL) requirements of the EU AI Act (Articles 14–15), EASA AI Roadmap 2.0 principles, and the programme's own Model Digital Constitution."),
        
        new Paragraph({ children: [new PageBreak()] }),
        heading("2  Core Principles", HeadingLevel.HEADING_1),
        para("NIBs are structurally derived from transformation contracts. They emerge where the BREX decision cascade cannot deterministically resolve an operation, making human oversight a consequence of epistemic limits rather than procedural ceremony."),
        
        new Paragraph({ children: [new PageBreak()] }),
        heading("3  Implementation", HeadingLevel.HEADING_1),
        para("NIB detection is implemented in the BREX Decision Engine runtime. When a NIB is triggered, the system follows a deterministic escalation protocol based on the classification matrix."),
        
        spacer(400),
        para("AEROSPACEMODEL-ASIT-NIB-SPEC-001 v1.0 DRAFT", { align: AlignmentType.CENTER, italics: true, color: "999999" }),
        para("© 2026 Amedeo Pelliccia / IDEALEeu Enterprise", { align: AlignmentType.CENTER, size: 16, color: "999999" }),
      ]
    }
  ]
});

// Generate and save
Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync("AEROSPACEMODEL-ASIT-NIB-SPEC-001.docx", buffer);
  console.log("✅ Document generated successfully");
  console.log("   Output: AEROSPACEMODEL-ASIT-NIB-SPEC-001.docx");
  console.log("   Size: " + (buffer.length / 1024).toFixed(1) + " KB\n");
}).catch(err => {
  console.error("❌ Error generating document:", err);
  process.exit(1);
});
