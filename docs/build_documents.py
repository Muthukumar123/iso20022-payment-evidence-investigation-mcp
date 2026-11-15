#!/usr/bin/env python3
"""Build a readable Word design package, PowerPoint deck and diagram PNGs.

Requirements: pip install python-docx python-pptx Pillow
Run: python docs/build_documents.py
Inputs are source Markdown and editable Mermaid files in docs/.
Generated assets are deterministic presentation artifacts, not bank data.
"""
from __future__ import annotations
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from docx import Document
from docx.shared import Inches as DI, Pt as DP, RGBColor as DR
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

BASE = Path(__file__).resolve().parent
OUTPUT = BASE / 'generated'
DRAWINGS = OUTPUT / 'diagrams'
OUTPUT.mkdir(parents=True, exist_ok=True)
DRAWINGS.mkdir(parents=True, exist_ok=True)
N = (22, 44, 71)
B = (47, 105, 155)
T = (11, 139, 145)
GRAY = (90, 109, 127)
LIGHT = (236, 244, 247)
WHITE = (255, 255, 255)


def ft(sz, strong=False):
    try:
        return ImageFont.truetype('DejaVuSans-Bold.ttf' if strong else 'DejaVuSans.ttf', sz)
    except OSError:
        return ImageFont.load_default()


def center_text(d, xy, s, size=22, fill=N, bold=False):
    d.text(xy, s, font=ft(size, bold), fill=fill, anchor='mm')


def arrow(d, x1, y1, x2, y2, color=B):
    d.line((x1, y1, x2, y2), fill=color, width=4)
    if abs(x2-x1) > abs(y2-y1):
        sg = 1 if x2 >= x1 else -1
        d.polygon([(x2,y2),(x2-sg*15,y2-8),(x2-sg*15,y2+8)],fill=color)
    else:
        sg = 1 if y2 >= y1 else -1
        d.polygon([(x2,y2),(x2-8,y2-sg*15),(x2+8,y2-sg*15)],fill=color)


def box(d, rect, text, dark=False):
    d.rounded_rectangle(rect, radius=18, fill=(T if dark else LIGHT), outline=(T if not dark else T), width=2)
    x1,y1,x2,y2 = rect
    center_text(d, ((x1+x2)//2, (y1+y2)//2), text, 22, WHITE if dark else N, True)


def architecture_png():
    im=Image.new('RGB',(1600,1070),'white')
    d=ImageDraw.Draw(im)
    center_text(d,(800,55),'ISO 20022 — Evidence-first Investigation Architecture',32,N,True)
    stages=[(410,110,1190,188,'Payment Operations Analyst'),
            (410,258,1190,336,'AI Agent / MCP Client'),
            (410,406,1190,484,'Private MCP Gateway [PROPOSED]'),
            (410,554,1190,632,'ISO 20022 MCP Server [PR #1 + PR #2]')]
    for i,rect in enumerate(stages):box(d,rect[:4],rect[4],dark=i in [1,3])
    for y in [188,336,484]:arrow(d,800,y+5,800,y+69)
    box(d,(45,732,760,812),'Evidence / Correlation [IMPLEMENTED]')
    box(d,(850,732,1555,812),'Read-only Bank Adapter [INTERFACE]')
    arrow(d,620,635,399,728)
    arrow(d,980,635,1199,728)
    for i,label in enumerate(['ISO Validation Core [PR #1]','Payment Hub REST / z/OS','MQ / SOAP / Batch']):
        x=40+i*537
        box(d,(x,919,x+460,1005),label)
    arrow(d,400,813,265,914)
    arrow(d,1199,813,808,914)
    arrow(d,1199,813,1344,914)
    path=DRAWINGS/'logical_architecture.png'
    im.save(path)
    return path


def parse_seq(src):
    participants=[];messages=[]
    for line in src.read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if line.startswith(('participant ','actor ')):
            m=re.match(r'(?:actor|participant)\s+(\w+)(?:\s+as\s+(.+))?',line)
            if m:participants.append((m.group(1),m.group(2) or m.group(1)))
        else:
            m=re.match(r'(\w+)(-->>|->>|-->|->)(\w+):\s*(.*)$',line)
            if m:messages.append((m.group(1),m.group(3),m.group(4),m.group(2).startswith('--')))
    return participants,messages


def seq_png(src):
    people, msgs=parse_seq(src)
    width=max(1700,350*len(people));height=235+len(msgs)*82
    im=Image.new('RGB',(width,height),'white')
    d=ImageDraw.Draw(im)
    center_text(d,(width//2,47),src.stem.replace('_',' ').title(),31,N,True)
    centers={k:int(160+i*(width-320)/max(1,len(people)-1)) for i,(k,_) in enumerate(people)}
    for k,label in people:
        x=centers[k]
        d.rounded_rectangle((x-135,101,x+135,186),radius=15,fill=N)
        words=label.replace('(future)','[proposed]').split()
        if len(' '.join(words))<=20:
            center_text(d,(x,145),' '.join(words),18,WHITE,True)
        else:
            half=(len(words)+1)//2
            center_text(d,(x,131),' '.join(words[:half])[:24],16,WHITE,True)
            center_text(d,(x,158),' '.join(words[half:])[:24],16,WHITE,True)
        d.line((x,188,x,height-39),fill=(198,213,224),width=2)
    for i,(src_id,dst_id,label,returning) in enumerate(msgs):
        y=243+i*82
        x1=centers[src_id];x2=centers[dst_id]
        c=T if returning else B
        if x1==x2:
            d.arc((x1-10,y-21,x1+100,y+29),245,120,fill=c,width=4)
            d.text((min(width-400,x1+60),y-44),label[:54],fill=N,font=ft(17))
        else:
            arrow(d,x1,y,x2,y,c)
            caption=label if len(label)<=53 else label[:50]+'...'
            tw=d.textbbox((0,0),caption,font=ft(17))
            tx=max(8,min(width-(tw[2]-tw[0])-8,(x1+x2)//2-(tw[2]-tw[0])//2))
            d.rectangle((tx-4,y-31,tx+tw[2]-tw[0]+4,y-6),fill='white')
            d.text((tx,y-29),caption,fill=N,font=ft(17))
        d.text((20,y-9),f'{i+1:02}',fill=GRAY,font=ft(17))
    output=DRAWINGS/(src.stem+'.png')
    im.save(output)
    return output


def add_shading(paragraph,fill='F2F5F7'):
    pp=paragraph._p.get_or_add_pPr()
    shd=OxmlElement('w:shd');shd.set(qn('w:fill'),fill);pp.append(shd)


def render_markdown(doc,source):
    lines=source.read_text(encoding='utf-8').splitlines()
    buf=[];table=[];code=[];in_code=False
    def flush_para():
        if buf:
            s=' '.join(buf).strip();buf.clear()
            if s:doc.add_paragraph(s)
    def flush_table():
        if not table:return
        rows=[]
        for r in table:
            cells=[s.strip() for s in r.strip().strip('|').split('|')]
            if all(re.fullmatch(r'[-: ]*',x) for x in cells):continue
            rows.append(cells)
        table.clear()
        if not rows:return
        count=min(5,max(map(len,rows)))
        t=doc.add_table(rows=0,cols=count)
        t.style='Light Shading Accent 1';t.alignment=WD_TABLE_ALIGNMENT.CENTER
        for ri,row in enumerate(rows):
            cells=t.add_row().cells
            for j in range(count):
                cells[j].text=(row[j] if j<len(row) else '')
                for p in cells[j].paragraphs:
                    for run in p.runs:run.font.size=DP(8)
            if ri==0:
                for cell in cells:
                    for p in cell.paragraphs:
                        for run in p.runs:run.bold=True
        doc.add_paragraph('')
    def flush_code():
        if not code:return
        for line in code:
            p=doc.add_paragraph(style='No Spacing')
            p.paragraph_format.left_indent=DI(.13)
            p.paragraph_format.right_indent=DI(.10)
            p.paragraph_format.space_after=DP(0)
            add_shading(p)
            # Break unreasonably long literal lines so they cannot escape the page.
            parts=[line[i:i+91] for i in range(0,len(line),91)] or ['']
            r=p.add_run('\n'.join(parts))
            r.font.name='Consolas';r.font.size=DP(7.3)
        code.clear()
        doc.add_paragraph('')
    for raw in lines:
        s=raw.strip()
        if s.startswith('```'):
            flush_para();flush_table()
            if in_code:flush_code()
            in_code=not in_code
            continue
        if in_code:
            code.append(raw.rstrip())
            continue
        if s.startswith('|'):
            flush_para();table.append(s);continue
        flush_table()
        if not s:
            flush_para();continue
        if s.startswith('#'):
            flush_para()
            depth=len(s)-len(s.lstrip('#'))
            title=s.lstrip('#').strip()
            doc.add_heading(title,min(depth,3) if depth>1 else 1)
            continue
        if s.startswith('- ') or re.match(r'^\d+\.\s+',s):
            flush_para()
            doc.add_paragraph(re.sub(r'^(?:[-*]|\d+\.)\s+','',s),style='List Bullet')
            continue
        if s.startswith('>'):
            flush_para()
            p=doc.add_paragraph(s.lstrip('> ').strip(),style='Quote')
            p.paragraph_format.left_indent=DI(.27)
            continue
        buf.append(s)
    flush_para();flush_table();flush_code()


def docx(images):
    document=Document()
    section=document.sections[0]
    section.top_margin=DI(.72);section.bottom_margin=DI(.68)
    section.left_margin=DI(.74);section.right_margin=DI(.74)
    styles=document.styles
    styles['Normal'].font.name='Aptos';styles['Normal'].font.size=DP(9.2)
    styles['Normal'].paragraph_format.space_after=DP(4)
    for name,size in [('Title',26),('Heading 1',16),('Heading 2',12.5),('Heading 3',10.7)]:
        styles[name].font.name='Aptos Display';styles[name].font.size=DP(size)
        styles[name].font.color.rgb=DR(*N)
    cover=document.add_paragraph('ISO 20022 Payment Intelligence',style='Title')
    cover.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p=document.add_paragraph('Solution Architecture • Core Banking & Legacy Integration • Complete Happy Path')
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p=document.add_paragraph('12 November 2026  |  Proof of concept  |  Synthetic payment data')
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    document.add_paragraph('Implemented: deterministic message validation and evidence correlation. Proposed: authenticated bank retrieval, gateway, live payment hubs and legacy connectors.')
    document.add_picture(str(images['logical_architecture']),width=DI(6.95))
    document.add_paragraph('Repository: github.com/Muthukumar123/iso20022-mcp • PR #1 + PR #2')
    document.add_page_break()
    document.add_heading('Part I — Solution Architecture and Integration',level=1)
    render_markdown(document,BASE/'ISO20022_MCP_Solution_Architecture.md')
    document.add_page_break()
    document.add_heading('Part II — Complete Happy-Path Tool Walkthrough',level=1)
    document.add_paragraph('The sequence diagram below describes the locally runnable flow with supplied synthetic XML. Bank retrieval is covered separately as a proposed architecture.')
    document.add_picture(str(images['happy_path_payment_sequence']),width=DI(6.85))
    render_markdown(document,BASE/'ISO20022_MCP_Happy_Path_Complete_Flow.md')
    document.add_page_break()
    document.add_heading('Appendix — Architecture Sequence Diagrams',level=1)
    for key,title in [('payment_investigation_sequence','Connected investigation (proposed bank adapters)'),('core_banking_api_sequence','Mainframe via z/OS Connect (proposed)'),('legacy_mq_sequence','Legacy IBM MQ (proposed)'),('repair_simulation_sequence','Safe repair simulation (proposed)')]:
        document.add_heading(title,level=2)
        document.add_picture(str(images[key]),width=DI(6.85))
    footer=section.footer.paragraphs[0]
    footer.text='ISO 20022 MCP • Architecture / Happy Path • Synthetic demonstration only'
    footer.alignment=WD_ALIGN_PARAGRAPH.CENTER
    out=OUTPUT/'ISO20022_MCP_Architecture_And_Happy_Path.docx'
    document.save(out)
    return out


def pptcol(t):return RGBColor(*t)

def text(slide,s,x,y,w,h,size=18,color=N,bold=False):
    box=slide.shapes.add_textbox(Inches(x),Inches(y),Inches(w),Inches(h))
    tf=box.text_frame;tf.word_wrap=True
    tf.margin_left=Inches(.045);tf.margin_top=Inches(.03)
    p=tf.paragraphs[0];p.text=s
    p.font.name='Aptos';p.font.size=Pt(size);p.font.bold=bold;p.font.color.rgb=pptcol(color)
    return box

def shape(slide,x,y,w,h,fill):
    obj=slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE,Inches(x),Inches(y),Inches(w),Inches(h))
    obj.fill.solid();obj.fill.fore_color.rgb=pptcol(fill);obj.line.color.rgb=pptcol(fill)
    return obj


def powerpoint(images):
    pres=Presentation();pres.slide_width=Inches(13.333);pres.slide_height=Inches(7.5)
    blank=pres.slide_layouts[6]
    def slide(title,context='REFERENCE ARCHITECTURE'):
        s=pres.slides.add_slide(blank)
        shape(s,0,0,13.333,.12,T)
        text(s,context,.66,.32,11,.27,10,T,True)
        text(s,title,.66,.78,12,.65,27,N,True)
        shape(s,.66,7.13,12,.02,(212,224,231))
        text(s,'ISO 20022 Payment Intelligence • Synthetic reference design',.67,7.18,12,.21,9,GRAY)
        return s
    def bullets(s,items,x=.94,y=1.75,width=11.2,line=.82,size=18):
        for i,item in enumerate(items):
            top=y+i*line
            shape(s,x,top+.17,.095,.095,T)
            text(s,item,x+.29,top,width-.29,line-.04,size,N)
    def graphic(title,key,subtitle=''):
        s=slide(title)
        im=Image.open(images[key]); iw,ih=im.size
        ratio=min(12.12/iw,5.42/ih)
        w=iw*ratio;h=ih*ratio
        s.shapes.add_picture(str(images[key]),Inches((13.333-w)/2),Inches(1.50+(5.42-h)/2),width=Inches(w),height=Inches(h))
        if subtitle:text(s,subtitle,.90,6.95,11,.18,10,GRAY)
        return s
    s=pres.slides.add_slide(blank)
    shape(s,0,0,13.333,7.5,N)
    shape(s,.72,1.04,.13,5.17,T)
    text(s,'PAYMENT INTELLIGENCE',1.14,1.13,11,.5,18,(112,229,224),True)
    text(s,'ISO 20022 MCP\nArchitecture + Happy Path',1.12,2.07,11,1.82,39,WHITE,True)
    text(s,'Evidence-backed investigation • Core banking • Legacy integration',1.14,4.53,10,.74,21,(219,233,242))
    text(s,'12 November 2026 | PR #1 + PR #2 | Synthetic example',1.14,6.57,10,.37,13,(185,210,221))
    s=slide('Why this is intelligent, not simply another XML parser')
    bullets(s,[
        'A single pacs.008 validation cannot prove that a bank rejected a payment.',
        'Correlate a pacs.002 with original message ID and exact transaction identifiers.',
        'Explain bank-reported status and mapped reasons with source field provenance.',
        'Say “unknown” for unknown codes; never invent account state or settlement status.',
        'Give a safe operations recommendation without executing any payment mutation.',
    ],line=.92)
    graphic('Reference architecture: implemented vs proposed','logical_architecture')
    s=slide('What exists today vs what is proposed')
    shape(s,.86,1.74,5.70,4.70,(229,244,241))
    shape(s,6.77,1.74,5.70,4.70,(232,241,248))
    text(s,'IMPLEMENTED / PR REVIEW',1.13,2.00,4.8,.37,19,T,True)
    text(s,'PROPOSED BANK INTEGRATION',7.07,2.00,5.1,.37,19,B,True)
    bullets(s,['XML business checks + optional XSD','MCP stdio tools + typed responses','Exact pacs.008 / pacs.002 correlation','Evidence ledger and safe next steps'],x=1.11,y=2.70,width=4.95,line=.82,size=16)
    bullets(s,['Private authenticated MCP gateway','Bank-owned REST / MQ / z/OS adapters','Authoritative source events and hashes','CBPR+/SEPA rules and enterprise audit'],x=7.05,y=2.70,width=5.07,line=.82,size=16)
    s=slide('Happy path A — locally runnable six-step flow','DETERMINISTIC DEMONSTRATION')
    rows=[('01','Agent initializes MCP + tools/list'),('02','Analyst supplies pacs.008 + pacs.002'),('03','validate_message checks XML, business, security'),('04','investigate_payment matches group + transaction IDs'),('05','lookup_code resolves reported AC04 reason'),('06','Agent explains evidence; human reviews next action')]
    for i,(no,line) in enumerate(rows):
        y=1.67+i*.84
        shape(s,.95,y,.70,.60,T);text(s,no,1.10,y+.13,.44,.34,17,WHITE,True)
        shape(s,1.82,y,10.45,.60,LIGHT);text(s,line,2.05,y+.13,9.97,.36,17,N)
    graphic('Sequence: actual local MCP tool orchestration','happy_path_payment_sequence')
    s=slide('Synthetic input: one payment and one status report')
    rows=[('pacs.008','GrpHdr/MsgId','MSG-DEMO-001'),('pacs.008','PmtId/EndToEndId','E2E-DEMO-001'),('pacs.008','PmtId/UETR','123e4567-e89b-42d3-a456-426614174000'),('pacs.002','OrgnlGrpInfAndSts/OrgnlMsgId','MSG-DEMO-001'),('pacs.002','TxInfAndSts/TxSts','RJCT'),('pacs.002','StsRsnInf/Rsn/Cd','AC04')]
    for i,(msg,key,val) in enumerate(rows):
        y=1.70+i*.79
        shape(s,.88,y,2.0,.61,LIGHT)
        text(s,msg,1.02,y+.13,1.75,.37,17,T,True)
        text(s,key,3.06,y+.12,5.25,.43,15,N)
        text(s,val,8.36,y+.12,4.25,.44,16,N,True)
    s=slide('Actual MCP request: tools/call investigate_payment')
    text(s,'The full XML strings are supplied as arguments. No bank lookup is implied.',.91,1.58,11.6,.45,17,GRAY)
    shape(s,.85,2.18,11.77,3.66,LIGHT)
    data='''{
  "jsonrpc": "2.0", "id": 3,
  "method": "tools/call",
  "params": {
    "name": "investigate_payment",
    "arguments": {
      "pacs008_xml": "<complete supplied pacs.008>",
      "pacs002_xml": "<complete supplied pacs.002>"
    }
  }
}'''
    text(s,data,1.16,2.39,10.8,3.20,18,N)
    s=slide('Result: verified correlation, not a guessed cause')
    cells=[('Correlation','MATCHED','GrpHdr/MsgId = OrgnlMsgId; EndToEndId matches'),('Bank-reported status','RJCT','pacs.002 TxInfAndSts[0]/TxSts'),('Bank-reported reason','AC04','pacs.002 StsRsnInf[0]/Rsn/Cd'),('Reference interpretation','Closed account','From maintained local code table'),('Safety decision','HUMAN REVIEW','No automatic retry or payment modification')]
    for i,(k,v,ev) in enumerate(cells):
        y=1.71+i*1.00
        shape(s,.94,y,11.45,.79,LIGHT)
        text(s,k,1.16,y+.09,3.4,.33,16,GRAY,True)
        text(s,v,4.40,y+.09,3.1,.35,18,T,True)
        text(s,ev,7.25,y+.07,4.90,.59,13,N)
    s=slide('Example analyst-facing answer')
    shape(s,.85,1.71,11.71,4.64,LIGHT)
    explanation='''Payment E2E-DEMO-001: bank-reported rejection. The pacs.002 matches the original message and EndToEndId. It contains RJCT and reason code AC04 (closed account). These are bank-reported facts, not independent confirmation of the beneficiary account state. Obtain verified replacement details via the approved customer process. Do not retry automatically. An authorized specialist must review any resubmission. Official XSD conformance is not established without the approved schemas.'''
    text(s,explanation,1.24,2.17,10.80,3.58,22,N)
    graphic('Happy path B — future connected bank investigation','payment_investigation_sequence')
    graphic('Core banking API sequence — z/OS Connect','core_banking_api_sequence')
    graphic('Legacy status retrieval — IBM MQ','legacy_mq_sequence')
    s=slide('Choosing the adapter for each legacy system')
    rows=[('REST / payment hub','Read-only HTTPS GET, scoped token + source event IDs'),('z/OS Connect / CICS','Expose approved COBOL/IMS/Db2 read programs as APIs'),('IBM MQ','Reply-to + correlation ID + TTL; timeout means unavailable'),('Event read model','Replay-safe history from Kafka/MQ; disclose freshness'),('SOAP / ESB / batch','Normalize to typed evidence and reconcile completeness')]
    for i,(name,desc) in enumerate(rows):
        y=1.70+i*.96
        shape(s,.89,y,3.65,.74,LIGHT)
        text(s,name,1.11,y+.16,3.16,.37,17,N,True)
        text(s,desc,4.83,y+.13,7.54,.56,17,N)
    s=slide('Data security and operations boundaries')
    bullets(s,[
        'Bank-owned IAM enforces principal, purpose, payment scope and least privilege.',
        'Payment execution, repair, settlement and resubmission stay outside MCP.',
        'Redact IBANs, names and remittance text before sending to external AI.',
        'Carry event ID, timestamp, message version and source digest in evidence.',
        'On no match, unknown code, stale status, or timeout: report uncertainty.',
    ],line=.94)
    graphic('Safe repair simulation — future human-controlled feature','repair_simulation_sequence')
    s=slide('What we can prove and what remains unproven')
    bullets(s,[
        'Proof with fixtures: AC04 / AM05; unknown ZZ99; mismatched message IDs.',
        'Exact identifiers prevent false attribution in these controlled scenarios.',
        'Implemented test suite, MCP tool discovery and CI support regression quality.',
        'Not yet proven: live bank integration, production accuracy or speed gains.',
        'Next pilot: bank-supplied sandbox records + operator-labeled evaluation set.',
    ],line=.95)
    s=slide('Implementation and adoption roadmap')
    rows=[('Phase 0','XML / security hardening','PR #1'),('Phase 1','Evidence-based investigation','PR #2'),('Phase 2','One bank sandbox read-only adapter','IAM + payment hub'),('Phase 3','Mainframe / MQ integration','Source ownership'),('Phase 4','Scheme rule intelligence + evaluation','SME governance'),('Phase 5','Bank-operated MCP gateway','Production approvals')]
    for i,(phase,name,status) in enumerate(rows):
        y=1.62+i*.83
        shape(s,.90,y,1.62,.59,T);text(s,phase,1.02,y+.11,1.4,.38,15,WHITE,True)
        text(s,name,2.78,y+.14,6.70,.43,17,N)
        text(s,status,9.35,y+.14,2.98,.44,15,B,True)
    out=OUTPUT/'ISO20022_Payment_Intelligence_Architecture.pptx'
    pres.save(out)
    return out,len(pres.slides)


def main():
    images={'logical_architecture':architecture_png()}
    for src in sorted((BASE/'diagrams').glob('*.mmd')):
        images[src.stem]=seq_png(src)
    word=docx(images)
    pptx,slides=powerpoint(images)
    print('DOCX:',word,'bytes',word.stat().st_size)
    print('PPTX:',pptx,'bytes',pptx.stat().st_size,'slides',slides)
    for name,fp in images.items():print('IMAGE:',name,fp)

if __name__=='__main__':main()