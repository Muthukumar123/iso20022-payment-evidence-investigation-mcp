/**
 * ISO 20022 Payment Intelligence — two-slide executive overview.
 * Reproducible: npm install pptxgenjs && node iso20022_executive_slides.js
 * Output: ISO20022_Payment_Intelligence_Executive_Overview.pptx
 * All diagrams are native, editable PowerPoint shapes.
 */
const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();
pptx.layout='LAYOUT_WIDE';
pptx.author='ISO 20022 MCP Project';
pptx.subject='Executive view of evidence-backed payment investigation and MCP integration';
pptx.title='ISO 20022 Payment Intelligence — Executive Overview';
pptx.company='ISO 20022 MCP Project';
pptx.lang='en-GB';
pptx.theme={headFontFace:'Aptos Display',bodyFontFace:'Aptos',lang:'en-GB'};
const C={navy:'132840',blue:'1B3855',teal:'009B9B',tealDark:'087B7C',mint:'ECF9F6',sky:'EEF5F9',line:'CDDAE3',grey:'556B7B',pale:'F7FAFC',white:'FFFFFF',amber:'B87414',sand:'FFF4E0',muted:'E9EFF2',green:'217F63'};
const W=13.333,H=7.5;
const R=pptx.ShapeType.roundRect,L=pptx.ShapeType.line;
function txt(slide,s,x,y,w,h,size=16,color=C.navy,bold=false,extra={}){slide.addText(s,{x,y,w,h,fontFace:'Aptos',fontSize:size,color,bold,margin:0,breakLine:false,fit:'shrink',...extra});}
function box(slide,x,y,w,h,fill=C.white,line=C.line,r=0.16){slide.addShape(R,{x,y,w,h,rectRadius:r,radius:r,fill:{color:fill},line:{color:line,width:1.1}});}
function line(slide,x1,y1,x2,y2,stroke=C.line,width=1.4,dash){slide.addShape(L,{x:x1,y:y1,w:x2-x1,h:y2-y1,line:{color:stroke,width,dashType:dash||'solid',beginArrowType:'none',endArrowType:'none'}});}
function arrow(slide,x1,y1,x2,y2,stroke=C.teal,width=1.8,dash){slide.addShape(L,{x:x1,y:y1,w:x2-x1,h:y2-y1,line:{color:stroke,width,dashType:dash||'solid',beginArrowType:'none',endArrowType:'triangle'}});}
function pill(slide,label,x,y,w,kind='teal'){const f=kind==='teal'?C.mint:kind==='blue'?C.sky:kind==='amber'?C.sand:C.muted; const t=kind==='teal'?C.tealDark:kind==='blue'?C.blue:kind==='amber'?C.amber:C.grey;box(slide,x,y,w,.32,f,f);txt(slide,label,x+.09,y+.07,w-.18,.18,9.5,t,true,{align:'center'});}
function bg(slide,section,title,sub){slide.background={color:C.white};slide.addShape(pptx.ShapeType.rect,{x:0,y:0,w:W,h:.10,line:{color:C.teal},fill:{color:C.teal}});txt(slide,section.toUpperCase(),.55,.30,11.5,.23,10,C.tealDark,true,{charSpacing:1.3});txt(slide,title,.55,.71,12.2,.58,27,C.navy,true);txt(slide,sub,.55,1.35,12.2,.55,13,C.grey,false);line(slide,.55,7.22,12.8,7.22,C.line,.7);txt(slide,'ISO 20022 PAYMENT INTELLIGENCE  •  EXECUTIVE VIEW  •  12 NOV 2026',.55,7.28,10.0,.14,8,C.grey);}
function numCircle(slide,number,x,y,color=C.teal){slide.addShape(pptx.ShapeType.ellipse,{x,y,w:.28,h:.28,line:{color},fill:{color}});txt(slide,String(number),x,y+.06,.28,.12,10,C.white,true,{align:'center'});}

// Slide 1 — business case and differentiated product
{
  const s=pptx.addSlide();bg(s,'01  /  Strategy','Not another XML parser. An explainable payment investigator.','Objective: turn pacs.008 and pacs.002 into a defensible answer to “Why was this payment rejected?”');
  // The contrast - need, approach, value
  box(s,.55,2.15,3.95,2.35,C.pale,C.line);pill(s,'COMMODITY TODAY',.76,2.33,1.53,'blue');
  txt(s,'Validate a message',.78,2.85,3.40,.38,20,C.navy,true);
  txt(s,'Parse XML • Check IBAN/BIC • Look up rejection codes',.78,3.35,3.33,.57,13,C.grey);
  txt(s,'Useful engineering utility; limited insight into an actual rejected payment.',.78,4.00,3.30,.36,11.3,C.grey);
  arrow(s,4.68,3.27,5.10,3.27,C.teal,2.4);
  box(s,5.18,2.15,7.58,2.35,C.mint,'C4E5DF');pill(s,'OUR PRODUCT DIRECTION',5.40,2.33,1.92,'teal');
  txt(s,'Investigate the payment lifecycle',5.42,2.85,6.92,.40,20,C.navy,true);
  txt(s,'Correlate messages by original ID + transaction ID, cite the bank-reported status and reason, separate facts from assumptions, and propose safe next steps.',5.42,3.34,6.80,.82,13,C.navy);
  // Value proposition flow
  txt(s,'THE BUSINESS FLOW',.55,4.78,7.9,.27,12,C.tealDark,true,{charSpacing:.9});
  const steps=[{h:'ASK',d:'Why rejected?'},{h:'RETRIEVE*',d:'pacs.008 + pacs.002'},{h:'PROVE',d:'Exact ID correlation'},{h:'EXPLAIN',d:'Status + evidence'},{h:'REVIEW',d:'Human-approved next step'}];
  const gap=.11,w=(12.21-4*gap)/5;
  steps.forEach((v,i)=>{const x=.55+i*(w+gap);box(s,x,5.20,w,1.05,i===2?C.mint:C.sky,i===2?'B2DCD2':C.line);txt(s,v.h,x+.12,5.39,w-.24,.22,13,i===2?C.tealDark:C.navy,true,{align:'center'});txt(s,v.d,x+.08,5.75,w-.16,.32,11.0,C.grey,false,{align:'center'});if(i<steps.length-1)arrow(s,x+w+.005,5.73,x+w+gap-.005,5.73,C.teal,1.2)});
  box(s,.55,6.48,12.2,.46,C.pale,C.pale);txt(s,'WHY IT MATTERS   Less manual investigation  •  Traceable, auditable findings  •  Reusable agent capabilities without autonomous payment changes',.72,6.61,11.85,.19,11.3,C.navy,true);
  txt(s,'* Bank retrieval is planned; today the demonstrated engine accepts supplied synthetic XML messages.',.55,7.00,12.1,.17,9.2,C.grey);
}
// Slide 2 — sequence, tools, and what exists
{
  const s=pptx.addSlide();bg(s,'02  /  Architecture & interaction','One controlled investigation, six MCP tools, explicit evidence.','Happy path: the AI orchestrates tools; deterministic code decides correlation; bank adapters provide authoritative records.');
  // Swimlanes
  const lanes=[{x:.60,w:1.92,title:'OPERATIONS'},{x:2.80,w:2.08,title:'AI AGENT'},{x:5.20,w:2.13,title:'MCP SERVICE'},{x:7.65,w:2.17,title:'EVIDENCE ENGINE'},{x:10.15,w:2.50,title:'BANK ADAPTER*'}];
  lanes.forEach((a,i)=>{box(s,a.x,2.16,a.w,.48,i===2?C.mint:C.sky,i===2?'B2DCD2':C.line);txt(s,a.title,a.x+.08,2.31,a.w-.16,.18,11,i===2?C.tealDark:C.navy,true,{align:'center'});line(s,a.x+a.w/2,2.66,a.x+a.w/2,5.53,C.line,.9,'dash')});
  // Sequence with arrows and explanatory labels
  arrow(s,1.58,3.10,2.92,3.10);txt(s,'1  “Why rejected?”',1.20,2.79,1.65,.18,10.2,C.grey);
  arrow(s,3.82,3.50,5.25,3.50);txt(s,'2  tools/list · validate_message',3.86,3.30,2.85,.17,10.2,C.navy);
  arrow(s,6.26,3.91,7.72,3.91);txt(s,'3  investigate_payment(XML×2)',6.05,3.71,2.92,.17,10.3,C.navy);
  arrow(s,8.75,4.34,6.28,4.34,C.teal);txt(s,'4  Match IDs · RJCT/AC04 · evidence',7.11,4.12,3.55,.17,10.0,C.grey);
  arrow(s,6.26,4.73,3.85,4.73,C.teal);txt(s,'5  Structured findings + limits',4.20,4.51,2.76,.17,10.0,C.grey);
  arrow(s,3.83,5.11,1.57,5.11,C.teal);txt(s,'6  Evidence + human action',2.25,4.92,2.20,.17,10.0,C.navy);
  // Dashed bank integration lane with bordered sub-note
  box(s,10.29,2.96,2.20,2.13,C.sand,'E6D6B8');pill(s,'FUTURE / PROPOSED',10.46,3.11,1.80,'amber');
  txt(s,'get_payment_evidence(ref)',10.47,3.58,1.84,.48,11.2,C.navy,true,{align:'center'});
  txt(s,'Bank-owned REST / SOAP / MQ / z/OS adapters',10.43,4.20,1.90,.57,10.3,C.grey,false,{align:'center'});
  arrow(s,10.22,3.55,9.48,3.55,C.amber,1.8,'dash');
  txt(s,'Today: analyst supplies XML; no live banking connection.',.60,5.63,7.6,.21,10.0,C.grey);
  // Tool inventory strip
  box(s,.55,5.98,12.20,1.01,C.pale,C.line);txt(s,'MCP TOOLKIT',.76,6.13,1.52,.22,11,C.tealDark,true); 
  txt(s,'parse_message   •   validate_message   •   investigate_payment   •   lookup_code   •   explain_message   •   generate_test_message',2.33,6.12,10.10,.47,12.2,C.navy,true);
  txt(s,'Executive control: evidence is observed; underlying cause is qualified; recommendations require human approval.',.76,6.72,11.75,.19,10.2,C.grey);
}
pptx.writeFile({fileName: process.env.OUTPUT_PPTX || 'ISO20022_Payment_Intelligence_Executive_Overview.pptx'});
