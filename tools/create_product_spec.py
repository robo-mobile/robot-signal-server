import os
from datetime import date
import logging
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, PageBreak, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch

PAGE_WIDTH = defaultPageSize[0]

log = logging.getLogger(__name__)


class PdfCreator:
    def __init__(self, workdir, version, release_date, changes, bugs):
        self.doc_path = workdir
        self.workdir = workdir
        self.version = version
        if release_date:
            self.release_date = release_date
        else:
            self.release_date = date.today().strftime('%Y/%m/%d')
        self.changes = changes
        self.bugs = bugs
        self.styles = getSampleStyleSheet()
        self.styleH = self.styles['Heading1']
        self.paragraph_style = ParagraphStyle('Text',
                                              fontName='Times-Roman',
                                              leading=15,
                                              fontSize=12,
                                              spaceBefore=10)
        self.list_style = ParagraphStyle('List',
                                         fontName='Times-Roman',
                                         spaceBefore=10,
                                         leading=15,
                                         fontSize=12,
                                         leftIndent=35)
        self.sublist_style = ParagraphStyle('SubList',
                                            fontName='Times-Roman',
                                            spaceBefore=10,
                                            leading=15,
                                            fontSize=12,
                                            leftIndent=50)
        self.story = []

    def print_centred_line(self, canvas, line, posy, style=None, size=None, isblack=True):
        if style is None:
            style = 'Times-Roman'
        if size is None:
            size = 12
        if isblack is True:
            canvas.setFillColor(colors.black)
        else:
            canvas.setFillColor(colors.darkblue)
        canvas.setFont(style, size)
        canvas.drawCentredString(PAGE_WIDTH / 2.0, posy * inch, line)

    def add_paragraph(self, title, text, style=None):
        if style is None:
            style = self.paragraph_style
        self.story.append(Paragraph('', self.paragraph_style))
        self.story.append(Paragraph(title, self.styleH))
        self.story.append(Paragraph(text, style))

    def add_list(self, lis, id='list', bulindent=20):
        for item in lis:
            if isinstance(item, list):
                self.add_list(item, 'sublist', 35)
            else:
                if lis.index(item) == (len(lis) - 1):
                    self.story.append(Paragraph(
                        f"<bullet bulletFontName='Times-Roman' indent={bulindent} fontSize=12 bulletColor='darkblue'>"
                        f"<seq id={id}>.<seqreset id={id}></bullet>{item}", self.list_style))
                else:
                    self.story.append(Paragraph(
                        f"<bullet bulletFontName='Times-Roman' indent={bulindent} fontSize=12 bulletColor='darkblue'>"
                        f"<seq id={id}>.</bullet>{item}", self.list_style))

    def release_maintanance_table(self):
        data = [['Product Name', 'Mine Detector'],
                ['Product Version', self.version],
                ['Release Date', self.release_date],]
        table = Table(data, colWidths=[100, 340])
        table.setStyle(TableStyle([('FONT', (0, 0), (1, 6), 'Times-Roman'),
                                   ('FONTSIZE', (0, 0), (1, 6), 12),
                                   ('FONT', (0, 0), (0, 6), 'Times-Bold'),
                                   ('VALIGN', (0, 0), (1, 6), 'TOP'),
                                   ('ALIGN', (0, 0), (1, 6), 'LEFT'),
                                   ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                   ('BOX', (0, 0), (-1, -1), 0.25, colors.black)
                                   ]))
        return table

    def title_page(self, canvas, doc):
        canvas.saveState()
        self.print_centred_line(canvas, f'Mine Detector {self.version}', 8, None, 48, False)
        canvas.drawInlineImage("./flir_cventaur.jpg", 0.5, 0.5)
        self.print_centred_line(canvas, 'Mine Detector Specification', 8, None, 48, False)
        self.print_centred_line(canvas, f'Copyright \251 {date.today().strftime("%Y")} Snail Ltd.', 1.25,
                                'Helvetica', 12, False)
        canvas.showPage()

    def notes_chapter(self):
        paragraph = f'''The release notes for Mine Detector {self.version}'''

        self.add_paragraph(f'Notes on Mine Detector {self.version}', paragraph)

    def introduction_chapter(self):
        paragraph = '''Mine Detector...'''

        self.add_paragraph(f'Introduction to Mine Detector {self.version}', paragraph)

    def release_maintanance_chapter(self):
        self.story.append(Paragraph('', self.paragraph_style))
        self.story.append(Paragraph('Release Maintenance', self.styleH))
        self.story.append(self.release_maintanance_table())
        self.story.append(PageBreak())

    def build_pdf(self):
        self.notes_chapter()
        self.introduction_chapter()
        self.release_maintanance_chapter()

    def create(self):
        self.build_pdf()
        SimpleDocTemplate(os.path.join(self.doc_path, self.version + ".pdf")).build(self.story,
                                                                                    onFirstPage=self.title_page)


some = PdfCreator(workdir='./', changes='', bugs='', version='0.0.1', release_date="")
some.create()
