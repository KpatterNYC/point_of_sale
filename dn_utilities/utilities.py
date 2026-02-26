from importlib import import_module
from io import BytesIO
from datetime import datetime

from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing

from reportlab.lib.units import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT



def get_form_class(app_label, form_name):
    """Dynamically import a form class from the app's forms.py"""
    module = import_module(f"{app_label}.forms")
    form_class = getattr(module, form_name)
    return form_class


class ReceiptGenerator:
    def __init__(self, receipt_data: dict, receipt_width_mm: int = 80):
        """
        Enhanced receipt_data structure:
        {
            "business_name": "Hub Name",
            "business_address": "Tom Mboya St, Nairobi",
            "business_phone": "+254700000000",
            "customer_name": "John Doe",
            "sale_id": "S12345",
            "timestamp": "2025-10-18 14:22",
            "products": [
                {
                    "name": "Samsung TV 55\" UHD Smart",
                    "attributes": {"Color": "Black", "Resolution": "3840x2160"},
                    "quantity": 1,
                    "unit_price": 68500
                }
            ],
            "subtotal": 65000,
            "total_amount": 68500,
            "logo_path": "static/imgs/logo.jpg",
            "thank_you": "Thank you for shopping with us!",
            "return_policy": "Items once sold can not be returned.",
            "served_by":"user_name"
        }
        """
        self.data = receipt_data
        self.width_mm = receipt_width_mm
        
        # More precise scaling for thermal printers
        self.scale = self.width_mm / 80.0
        self.font_sizes = {
            "header": max(10 * self.scale, 8),  # Minimum font size
            "normal": max(8 * self.scale, 7),
            "small": max(7 * self.scale, 6),
            "xsmall": max(6 * self.scale, 5),
        }

        # Dynamic page size - will be calculated based on content
        self.page_size = (self.width_mm * mm, 400 * mm)  # Initial height, will adjust
        
        # Thermal printer optimized margins
        self.margins = {
            "left": max(3 * self.scale, 2) * mm,
            "right": max(3 * self.scale, 2) * mm,
            "top": max(3 * self.scale, 2) * mm,
            "bottom": max(3 * self.scale, 2) * mm,
        }

        self.buffer = BytesIO()
        self.flow = []
        self.stylesheet = getSampleStyleSheet()
        self._define_styles()

    def _define_styles(self):
        """Define styles with thermal printer optimization"""
        # Use monospaced font for clean alignment
        monospace_font = "Courier"
        
        self.stylesheet.add(
            ParagraphStyle(
                name="r_header",
                fontName=f"{monospace_font}-Bold",
                fontSize=self.font_sizes["header"],
                alignment=TA_CENTER,
                spaceAfter=1 * mm * self.scale,
            )
        )
        self.stylesheet.add(
            ParagraphStyle(
                name="r_subheader",
                fontName=monospace_font,
                fontSize=self.font_sizes["normal"],
                alignment=TA_CENTER,
                spaceAfter=0.5 * mm * self.scale,
            )
        )
        self.stylesheet.add(
            ParagraphStyle(
                name="r_normal",
                fontName=monospace_font,
                fontSize=self.font_sizes["normal"],
                alignment=TA_LEFT,
                leading=self.font_sizes["normal"] * 1.2,
            )
        )
        self.stylesheet.add(
            ParagraphStyle(
                name="r_small",
                fontName=monospace_font,
                fontSize=self.font_sizes["small"],
                alignment=TA_LEFT,
                leading=self.font_sizes["small"] * 1.1,
            )
        )
        self.stylesheet.add(
            ParagraphStyle(
                name="r_xsmall",
                fontName=monospace_font,
                fontSize=self.font_sizes["xsmall"],
                alignment=TA_LEFT,
                leading=self.font_sizes["xsmall"] * 1.1,
            )
        )
        self.stylesheet.add(
            ParagraphStyle(
                name="r_right",
                fontName=monospace_font,
                fontSize=self.font_sizes["normal"],
                alignment=TA_RIGHT,
            )
        )
    def _header_section(self):
        """Generate header with QR code centered at the top"""
        d = self.data
        business_name = d.get("business_name", "")
        sale_id = d.get("sale_id", "N/A")

        # 1. Generate and Center QR Code
        try:
            qr_content = f"ID:{sale_id}\nStore:{business_name}\nTotal:{d.get('total_amount')}"
            qr_size = 25 * mm * self.scale
            
            qr_code = qr.QrCodeWidget(qr_content)
            qr_code.barWidth = qr_size
            qr_code.barHeight = qr_size
            qr_code.qrVersion = 1
            
            qr_drawing = Drawing(qr_size, qr_size)
            qr_drawing.add(qr_code)

            # We use a Table to force perfect horizontal centering
            qr_table = Table([[qr_drawing]], colWidths=[self.width_mm * mm])
            qr_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2 * mm),
            ]))
            
            self.flow.append(qr_table)
        except Exception as e:
            print(f"QR Generation error: {e}")

        # 2. Business Name (Centered)
        if business_name:
            header_style = self.stylesheet["r_header"].clone('r_header_dynamic')
            if len(business_name) > 25:
                header_style.fontSize = max(self.font_sizes["header"] - 2, 6)
            
            self.flow.append(Paragraph(f"<b>{business_name}</b>", header_style))

        # 3. Business Address (Centered)
        if addr := d.get("business_address"):
            self.flow.append(Paragraph(addr, self.stylesheet["r_subheader"]))

        self.flow.append(Spacer(1, 3 * mm * self.scale))


    def _customer_info(self):
        """Generate customer and sale information"""
        d = self.data
        
        # Separator line
        self._separator()
        self.flow.append(Spacer(1, 2 * mm * self.scale))
        
        if d.get("customer_name") or d.get("sale_id"):
            info_lines = []
            if d.get("customer_name"):
                info_lines.append(f"Customer Name: {d['customer_name']}")
            # ✅ Add Customer Phone
            if d.get("customer_phone"):
                info_lines.append(f"Customer Tel: {d['customer_phone']}")
            if d.get("sale_id"):
                info_lines.append(f"Receipt ID: {d['sale_id']}")
            
            ts = d.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M")
            info_lines.append(f"Date: {ts}")
            
            for line in info_lines:
                self.flow.append(Paragraph(line, self.stylesheet["r_small"]))
            
            self.flow.append(Spacer(1, 3 * mm * self.scale))

    def _format_attrs(self, attrs: dict) -> str:
        if isinstance(attrs, dict):
            return "".join(f"• {k}: {v}<br/>" for k, v in attrs.items())
        if isinstance(attrs, list):
            return "".join(f"• {a}<br/>" for a in attrs)
        return str(attrs)
    

    def _product_lines(self):
        """Generate product listing with better alignment"""
        self.flow.append(Paragraph("<b>ITEMS PURCHASED</b>", self.stylesheet["r_normal"]))
        self.flow.append(Spacer(1, 2 * mm * self.scale))
        
        # Calculate subtotal if not provided
        calculated_subtotal = sum(
            p.get("quantity", 1) * p.get("unit_price", 0) 
            for p in self.data.get("products", [])
        )
        
        for i, p in enumerate(self.data.get("products", []), start=1):
            name = p.get("name", "Unnamed Product")
            qty = int(p.get("quantity", 1))
            unit_price = float(p.get("unit_price", 0))
            line_total = qty * unit_price

            # Product name and number
            self.flow.append(Paragraph(f"{i}. <b>{name}</b>", self.stylesheet["r_normal"]))
            
            # Product attributes
            attrs = p.get("attributes")
            if attrs:
                attr_text = self._format_attrs(attrs)
                self.flow.append(Paragraph(f"   {attr_text}", self.stylesheet["r_xsmall"]))
            
            # Quantity and pricing - better aligned
            price_line = f"   Qty: {qty} × {unit_price:,.0f} = {line_total:,.0f}"
            self.flow.append(Paragraph(price_line, self.stylesheet["r_small"]))
            
            self.flow.append(Spacer(1, 1.5 * mm * self.scale))

        self.flow.append(Spacer(1, 2 * mm * self.scale))
        
        # Store calculated subtotal if not provided in data
        if not self.data.get("subtotal"):
            self.data["subtotal"] = calculated_subtotal
    def _total_section(self):
        """Generate totals with subtotal, tax, and grand total"""
        subtotal = float(self.data.get("subtotal", 0))
        total = float(self.data.get("total_amount", subtotal))
        
        self._separator()
        self.flow.append(Spacer(1, 1 * mm * self.scale))
        
        # Wrap cells in Paragraph so <b> markup works
        totals_data = [
            [
                Paragraph("<b>TOTAL:</b>", self.stylesheet["r_normal"]),
                Paragraph(f"<b>KES {total:,.0f}</b>", self.stylesheet["r_right"]),
            ],
        ]
        
        totals_table = Table(
            totals_data,
            colWidths=[self.width_mm * mm * 0.5, self.width_mm * mm * 0.4]
        )
        
        totals_table.setStyle(TableStyle([
            ('FONT', (0, 0), (-1, -1), 'Courier'),
            ('FONTSIZE', (0, 0), (-1, -1), self.font_sizes["normal"]),
            ('ALIGN', (0, 0), (0, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 1),
        ]))
        
        self.flow.append(totals_table)
        self.flow.append(Spacer(1, 3 * mm * self.scale))
    def _footer(self):
        """Generate footer with thank you message, policies, and served_by info"""
        self._separator()

        msg = self.data.get("thank_you", "Thank you for your business!")
        self.flow.append(Paragraph(msg, self.stylesheet["r_small"]))

        return_policy = self.data.get("return_policy")
        if return_policy:
            self.flow.append(Spacer(1, 1 * mm * self.scale))
            self.flow.append(Paragraph(return_policy, self.stylesheet["r_xsmall"]))

        # ✅ Add served_by line if present
        served_by = self.data.get("served_by")
        if served_by:
            self.flow.append(Spacer(1, 2 * mm * self.scale))
            self.flow.append(
                Paragraph(f"Served by: <b>{served_by}</b>", self.stylesheet["r_xsmall"])
            )

        # Keep existing footer
        self.flow.append(Spacer(1, 2 * mm * self.scale))
        self.flow.append(Paragraph("Powered by <b>CleanCode</b>", self.stylesheet["r_xsmall"]))

        
    def _separator(self):
        """Add a dotted separator line"""
        dot_line = "=" * int(47 * self.scale)
        self.flow.append(Paragraph(dot_line.strip(), self.stylesheet["r_small"]))
        self.flow.append(Spacer(1, 2 * mm * self.scale))
        
    
    def build_pdf_bytes(self) -> BytesIO:
        self.flow = []
        
        # 1. Build sections
        self._header_section()
        self._customer_info()
        self._product_lines()
        self._total_section()
        self._footer()

        # 2. Precise Height Calculation
        # Make sure to subtract margins exactly as doc template does
        available_width = (self.width_mm * mm) - (self.margins['left'] + self.margins['right'])
        total_height = 0
        
        for flowable in self.flow:
            # We use wrap() to simulate the layout
            w, h = flowable.wrap(available_width, 2000 * mm) # Use a very tall limit
            total_height += h

        # 3. Add a more generous buffer (10mm - 15mm) for thermal printers
        # This accounts for the space between flowables (leading/spacers)
        final_height = total_height + self.margins['top'] + self.margins['bottom'] + (10 * mm)

        self.buffer = BytesIO()
        doc = SimpleDocTemplate(
            self.buffer,
            pagesize=(self.width_mm * mm, final_height),
            # Ensure these margins match the ones used in the wrap() calculation
            leftMargin=self.margins["left"],
            rightMargin=self.margins["right"],
            topMargin=self.margins["top"],
            bottomMargin=self.margins["bottom"],
        )
        
        # IMPORTANT: This prevents ReportLab from trying to balance pages
        doc.allowSplitting = False 
        
        doc.build(self.flow)
        self.buffer.seek(0)
        return self.buffer
    # def build_pdf_bytes(self) -> BytesIO:
    #     """Build the PDF and return bytes"""
    #     self.flow = []
        
    #     # Build all sections
    #     self._header_section()
    #     self._customer_info()
    #     self._product_lines()
    #     self._total_section()
    #     self._footer()

    #     # Create document with thermal-printer optimized settings
    #     doc = SimpleDocTemplate(
    #         self.buffer,
    #         pagesize=self.page_size,
    #         leftMargin=self.margins["left"],
    #         rightMargin=self.margins["right"],
    #         topMargin=self.margins["top"],
    #         bottomMargin=self.margins["bottom"],
    #     )
        
    #     doc.build(self.flow)
    #     self.buffer.seek(0)
    #     return self.buffer

    def save_to_file(self, filename: str) -> str:
        """Save PDF to file"""
        buf = self.build_pdf_bytes()
        with open(filename, "wb") as f:
            f.write(buf.read())
        return filename

    def get_pdf_bytes(self) -> bytes:
        """Get PDF as bytes for immediate use"""
        buf = self.build_pdf_bytes()
        return buf.getvalue()