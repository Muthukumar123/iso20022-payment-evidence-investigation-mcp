/**
 * Payment Evidence Intelligence (PEI) — 7-slide board / architecture briefing
 * Native editable PowerPoint; all diagrams are shapes/text.
 * Build: npm install --no-save pptxgenjs@4.0.0
 *        node docs/executive/build_executive_slides.js
 */
const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();
pptx.layout='LAYOUT_WIDE';
pptx.author='ISO 20022 MCP Project';
pptx.subject='PEI executive business case: why AI, why MCP, tool catalog, sequence, risk and value';
pptx.title='Payment Evidence Intelligence | Executive Architecture';
pptx.company='ISO 20022 MCP Project';
pptx.lang='en-GB';
pptx.theme={headFontFace:'Aptos Display',bodyFontFace:'Aptos',lang:'en-GB'};
const W=13.333,H=7.5;
const C={navy:'13283F',ink:'172F49',steel:'496275',teal:'0C8E91',darkTeal:'087578',mint:'EAF7F3',mintLine:'B6DDD4',blue:'EAF1F8',blueLine:'C8D6E5',white:'FFFFFF',pale:'F7FAFC',grey:'64798A',line:'D6E0E7',amber:'9B6211',sand:'FFF2DC',orangeLine:'E6D1A7',red:'A63F40',redBg:'FBEDEE',green:'217A5C',greenBg:'E9F7F0',slate:'31465B'};
const Shape=pptx.ShapeType;
function text(sl,s,x,y,w,h,size=14,color=C.navy,bold=false,extra={}) {sl.addText(s,{x,y,w,h,fontFace: 'Aptos', fontSize:size,color,bold,margin:0,breakLine:false,fit:'shrink',valign:'mid',...extra});}
function rect(sl,x,y,w,h,fill=C.white,stroke=C.line,round=0.16,sw=1) {sl.addShape(Shape.roundRect,{x,y,w,h,rectRadius:round,radius:round,fill:{color:fill},line:{color:stroke,width:sw}});}
function rule(sl,x1,y1,x2,y2,color=C.line,thick=1,dash=false){sl.addShape(Shape.line,{x:x1,y:y1,w:x2-x1,h:y2-y1,line:{color,width:thick,dashType:dash?'dash':'solid'}});}
function arrow(sl,x1,y1,x2,y2,color=C.teal,thick=1.6,dash=false) {sl.addShape(Shape.line,{x:x1,y:y1,w:x2-x1,h:y2-y1,line:{color,width:thick,dashType:dash?'dash':'solid',endArrowType:'triangle'}});}
function label(sl,txt,x,y,w,kind='teal'){let colors=kind==='amber'?[C.sand,C.amber,C.orangeLine]:kind==='red'?[C.redBg,C.red,'E9BCBF']:kind==='grey'?[C.pale,C.grey,C.line]:kind==='blue'?[C.blue,C.ink,C.blueLine]:[C.mint,C.darkTeal,C.mintLine];rect(sl,x,y,w,.30,colors[0],colors[2],.14,.9);text(sl,txt,x+.05,y+.065,w-.10,.16,9.3,colors[1],true,{align:'center'});}
function section(sl,n,kicker,title,subtitle){sl.background={color:C.white};sl.addShape(Shape.rect,{x:0,y:0,w:W,h:.11,line:{color:C.teal},fill:{color:C.teal}});text(sl,`PEI  /  ${kicker.toUpperCase()}`,.56,.29,10,.26,10,C.darkTeal,true,{charSpacing:1.1});text(sl,title,.56,.71,12.05,.51,25.5,C.navy,true);text(sl,subtitle,.56,1.27,12.08,.46,12.7,C.grey);rule(sl,.56,7.19,12.79,7.19,C.line,.8);text(sl,'PAYMENT EVIDENCE INTELLIGENCE  •  EXECUTIVE CONCEPT  •  12 NOV 2026',.56,7.27,10.9,.12,8.1,C.grey);text(sl,`${n} / 7`,12.03,7.26,.75,.14,8.8,C.grey,true,{align:'right'});}
function bullet(sl,head,detail,x,y,w,opt={}) {const {h=.73,shade=C.pale,stroke=C.line,headSize=14,bodySize=10.5}=opt;rect(sl,x,y,w,h,shade,stroke);text(sl,head,x+.14,y+.13,w-.28,.22,headSize,C.navy,true);text(sl,detail,x+.14,y+.39,w-.28,h-.49,bodySize,C.grey);}
function circle(sl,n,x,y,color=C.teal){sl.addShape(Shape.ellipse,{x,y,w:.32,h:.32,line:{color},fill:{color}});text(sl,String(n),x+.01,y+.082,.30,.13,10.2,C.white,true,{align:'center'});}
function heading(sl,s,x,y,w){text(sl,s,x,y,w,.27,12,C.darkTeal,true,{charSpacing:.8});}
function small(sl,s,x,y,w,h=0.32){text(sl,s,x,y,w,h,10,C.grey);}

// Slide 1 — concise investment thesis / value.
{
 const s=pptx.addSlide();section(s,1,'investment thesis','Payment Evidence Intelligence (PEI)','AI-assisted payment investigations — evidence before explanations, humans before payment actions.');
 label(s,'THE PROBLEM',.62,1.89,1.55,'amber');
 rect(s,.62,2.32,3.55,2.41,C.pale,C.line);
 text(s,'Payment exceptions are fragmented',.84,2.56,3.08,.62,19,C.navy,true);
 text(s,'Analysts manually compare payment messages, rejection codes, scheme rules and system histories.',.84,3.28,3.02,.85,14,C.steel);
 label(s,'THE CONCEPT',4.55,1.89,1.63,'teal');
 rect(s,4.55,2.32,4.22,2.41,C.mint,C.mintLine);
 text(s,'An evidence-first investigator',4.78,2.57,3.75,.40,19,C.navy,true);
 text(s,'An AI agent asks the right questions and invokes governed tools; deterministic services correlate pacs.008 and pacs.002, trace sources and qualify uncertainty.',4.78,3.16,3.72,1.25,13.1,C.ink);
 label(s,'EXPECTED VALUE',9.16,1.89,1.64,'blue');
 rect(s,9.16,2.32,3.54,2.41,C.blue,C.blueLine);
 text(s,'Faster, more consistent decisions',9.39,2.57,3.04,.65,18.5,C.navy,true);
 text(s,'Less manual evidence collection; reproducible explanations; clearer escalation paths.',9.39,3.37,3.02,.84,13.6,C.steel);
 heading(s,'WHAT IS DISTINCTIVE',.64,5.08,4.5);
 const x0=.62,w=3.91,gap=.29;[
  ['Cross-message correlation','Match original message ID + exact transaction identifiers.'],
  ['Provenance, not guesses','Source fields and unknown-code handling are explicit.'],
  ['Safe human-in-the-loop','No automated resend, mutation or account-status assumption.']
 ].forEach((a,i)=>{const x=x0+i*(w+gap);rect(s,x,5.53,w,.97,i===1?C.mint:C.pale,i===1?C.mintLine:C.line);text(s,a[0],x+.15,5.70,w-.30,.22,14.5,C.navy,true);text(s,a[1],x+.15,6.04,w-.30,.28,11.2,C.grey)});
 small(s,'Product objective, not a measured bank outcome. Current demo uses supplied XML; live payment-system connectivity is proposed.',.62,6.68,12.0,.24);
}
// Slide 2 — compare conventional, AI and MCP.
{
 const s=pptx.addSlide();section(s,2,'why ai & mcp','Why AI + MCP instead of a single REST API?','A REST API is sufficient for fixed validation. AI and MCP add value when investigative questions and tool paths vary.');
 const cards=[
 {x:.62,title:'Traditional API / workflow',flag:'DETERMINISTIC',kind:'blue',lines:['Application selects a fixed endpoint','Rules check known fields and codes','A developer wires the investigation path'],b:'Best for predictable processing'},
 {x:4.85,title:'AI agent + direct APIs',flag:'FLEXIBLE, CUSTOM',kind:'grey',lines:['AI interprets varied analyst questions','Custom API/tool wrappers per AI client','Agent synthesizes authorized results'],b:'Useful, but bespoke integration'},
 {x:9.08,title:'AI agent + MCP',flag:'REUSABLE TOOL CONTRACT',kind:'teal',lines:['AI discovers available tools/schemas','Standardized, governed tool invocation','Multiple clients reuse the same tools'],b:'Best for multi-tool agent workflows'}
 ];
 cards.forEach((a,i)=>{rect(s,a.x,2.03,3.65,3.18,i===2?C.mint:C.pale,i===2?C.mintLine:C.line);label(s,a.flag,a.x+.18,2.22,i===2?2.19:1.69,a.kind);text(s,a.title,a.x+.19,2.75,3.24,.52,18,C.navy,true);a.lines.forEach((x,j)=>{slDot(s,a.x+.25,3.40+j*.42,i===2?C.teal:C.steel);text(s,x,a.x+.45,3.32+j*.42,2.94,.34,11.25,C.steel)});rule(s,a.x+.20,4.70,a.x+3.45,4.70,C.line,1);text(s,a.b,a.x+.20,4.82,3.22,.21,11.2,i===2?C.darkTeal:C.grey,true)});
 rect(s,.62,5.47,12.10,1.00,C.blue,C.blueLine);
 text(s,'Division of responsibilities',.82,5.67,2.45,.27,14.0,C.ink,true);
 text(s,'AI = interpret intent and explain evidence   •   MCP = discover & invoke tools   •   Banking services = deterministic truth & authorization',3.20,5.67,9.18,.51,13.1,C.ink,true);
 small(s,'MCP is not a replacement for REST, a payment hub, rule engines or controls. A single REST endpoint remains the right choice for a fixed XML-validation use case.',.64,6.71,12.0,.31);
}
function slDot(s,x,y,c){s.addShape(Shape.ellipse,{x,y,w:.10,h:.10,line:{color:c},fill:{color:c}})}
// Slide 3 — architecture and trust boundary.
{
 const s=pptx.addSlide();section(s,3,'target architecture','One business engine, two interfaces — standard API + MCP','Reuse the same deterministic financial logic; make the agent an assisted investigation surface, not the system of record.');
 const y=2.04;
 rect(s,.60,y,2.33,2.11,C.blue,C.blueLine);text(s,'ANALYST',.80,y+.22,1.93,.25,11,C.darkTeal,true);text(s,'Natural-language question',.80,y+.59,1.93,.60,17,C.navy,true);text(s,'“Why did REF123 fail?”',.80,y+1.49,1.94,.30,11.3,C.grey);
 arrow(s,2.99,3.09,3.41,3.09);
 rect(s,3.48,y,2.46,2.11,C.pale,C.line);text(s,'AI AGENT',3.68,y+.22,2.08,.25,11,C.darkTeal,true);text(s,'Select tools and synthesize evidence',3.68,y+.63,2.08,.88,15.4,C.navy,true);text(s,'No settlement rights',3.68,y+1.62,2.08,.23,10.8,C.grey);
 arrow(s,6.01,3.09,6.44,3.09);
 rect(s,6.52,y,2.64,2.11,C.mint,C.mintLine);text(s,'MCP ADAPTER',6.72,y+.22,2.25,.25,11,C.darkTeal,true);text(s,'Discover & call six tools',6.72,y+.63,2.25,.75,16,C.navy,true);text(s,'stdio today; remote gateway proposed',6.72,y+1.51,2.22,.34,10.1,C.grey);
 arrow(s,9.23,3.09,9.65,3.09);
 rect(s,9.74,y,2.96,2.11,C.blue,C.blueLine);text(s,'ISO 20022 CORE',9.95,y+.22,2.55,.25,11,C.darkTeal,true);text(s,'Parse · validate · correlate · cite',9.95,y+.64,2.55,.75,15.0,C.navy,true);text(s,'XSD optional; source evidence explicit',9.95,y+1.53,2.55,.33,10.4,C.grey);
 rule(s,.62,4.53,12.70,4.53,C.line,1);
 heading(s,'BANKING TRUST BOUNDARY — TARGET ONLY',.65,4.80,7.3);
 rect(s,.64,5.22,5.75,1.13,C.sand,C.orangeLine);text(s,'Controlled bank-owned adapter + gateway',.84,5.41,5.32,.31,14.2,C.navy,true);text(s,'OIDC/RBAC · read-only service identity · auditing · masking',.84,5.83,5.25,.22,11.3,C.amber);
 arrow(s,6.47,5.80,7.04,5.80,C.amber,1.7,true);
 rect(s,7.15,5.22,5.55,1.13,C.pale,C.line);text(s,'Payment hub · Core banking · MQ · SOAP · Archive',7.36,5.40,5.12,.37,13.7,C.navy,true);text(s,'Authoritative read responses, not agent-generated status',7.36,5.87,5.04,.21,10.9,C.grey);
 small(s,'Glama is optional catalog / publishing infrastructure, not part of the bank-data runtime path. Live banking adapters are not implemented.',.64,6.67,12.0,.28);
}
// Slide 4 — full toolbox.
{
 const s=pptx.addSlide();section(s,4,'tool inventory','Six working tools. Banking data tools are the next milestone.','Implemented MCP methods operate on supplied XML; proposed adapters would retrieve approved live evidence.');
 heading(s,'IMPLEMENTED  /  ACTUAL SERVER TOOLS',.65,1.89,7.85);
 const tools=[
 ['parse_message','Extract message identifiers, parties and transaction fields'],
 ['validate_message','Business rules, optional XSD and security findings'],
 ['investigate_payment','Cross-message correlation and provenance ledger'],
 ['lookup_code','Known reason/status code meaning; unknown = unknown'],
 ['explain_message','Deterministic plain-language message explanation'],
 ['generate_test_message','Synthetic test messages and defect scenarios']
 ];
 tools.forEach((a,i)=>{let col=i%2,row=Math.floor(i/2),x=.65+col*4.2,y=2.30+row*1.15;rect(s,x,y,4.03,1.00,i===2?C.mint:C.pale,i===2?C.mintLine:C.line);text(s,a[0],x+.18,y+.17,3.68,.24,15,C.navy,true);text(s,a[1],x+.18,y+.53,3.63,.27,10.85,C.steel)});
 rect(s,9.31,1.88,3.38,3.84,C.sand,C.orangeLine);label(s,'PROPOSED — NOT AVAILABLE',9.50,2.11,2.75,'amber');text(s,'Bank-connected tools',9.53,2.64,2.90,.34,17.2,C.navy,true);
 const future=['get_payment_evidence(ref)','get_payment_status(ref)','get_scheme_rules(rail,date)','check_duplicate_payment(ids)','simulate_repair(candidate)'];future.forEach((a,i)=>{slDot(s,9.56,3.20+i*.42,C.amber);text(s,a,9.77,3.10+i*.42,2.73,.27,11.5,C.ink,true)});
 rect(s,.65,5.98,12.04,.64,C.blue,C.blueLine);text(s,'Why tools matter:',.85,6.18,1.75,.23,13.0,C.ink,true);text(s,'AI selects the right capabilities; MCP standardizes calls; deterministic engines produce the evidence and validation result.',2.65,6.17,9.70,.27,12.1,C.ink);
 small(s,'No tool can authorize payment execution. Names under “proposed” are architectural concepts, not callable methods in the current repository.',.65,6.77,11.90,.22);
}
// Slide 5 — explicit interaction sequence.
{
 const s=pptx.addSlide();section(s,5,'end-to-end happy path','Example: REF123 rejected — show the evidence chain','Local demo uses supplied synthetic pacs.008 + pacs.002. Live retrieval through the bank would be an additional tool.');
 const lane=[{x:.68,w:1.83,t:'OPERATIONS'},{x:2.71,w:2.17,t:'AI AGENT'},{x:5.13,w:2.28,t:'MCP SERVER'},{x:7.65,w:2.20,t:'EVIDENCE CORE'}];
 lane.forEach((a,i)=>{rect(s,a.x,1.97,a.w,.43,i===2?C.mint:C.blue,i===2?C.mintLine:C.blueLine);text(s,a.t,a.x+.05,2.10,a.w-.1,.15,10.4,C.navy,true,{align:'center'});rule(s,a.x+a.w/2,2.40,a.x+a.w/2,5.78,C.line,.75,true)});
 const steps=[
  {y:2.79,x1:1.60,x2:2.80,label:'1  “Why rejected?”'},
  {y:3.28,x1:3.86,x2:5.23,label:'2  tools/list + validate_message'},
  {y:3.77,x1:6.25,x2:7.72,label:'3  investigate_payment(XML×2)'},
  {y:4.26,x1:8.76,x2:6.27,label:'4  Correlate IDs + code lookup'},
  {y:4.75,x1:6.24,x2:3.85,label:'5  Return evidence and limitations'},
  {y:5.24,x1:3.80,x2:1.59,label:'6  Human-reviewed explanation'}
 ];
 steps.forEach((a,i)=>{const cx=(a.x1+a.x2)/2;const w=i===2?2.40:i===3?2.42:i===4?2.33:2.23;arrow(s,a.x1,a.y,a.x2,a.y,i===3?C.teal:C.darkTeal,1.6);text(s,a.label,cx-w/2,a.y-.25,w,.17,10.0,i===3?C.teal:C.navy,true,{align:'center'})});
 rect(s,10.18,2.01,2.49,3.48,C.pale,C.line);label(s,'SYNTHETIC CASE',10.37,2.20,2.02,'blue');text(s,'Original pacs.008',10.39,2.72,1.98,.27,12.5,C.navy,true);text(s,'MsgId=MSG-123\nEndToEndId=E2E-123',10.39,3.06,1.98,.57,11.4,C.steel);rule(s,10.39,3.72,12.40,3.72,C.line,1);text(s,'Bank-reported pacs.002',10.39,3.84,1.98,.27,12.5,C.navy,true);text(s,'OrgnlMsgId=MSG-123\nOrgnlEndToEndId=E2E-123\nTxSts=RJCT · AC04',10.39,4.18,2.04,.81,11.3,C.steel);
 rect(s,.67,6.01,12.0,.65,C.mint,C.mintLine);text(s,'OUTPUT',.86,6.22,1.10,.19,11.4,C.darkTeal,true);text(s,'Matched payment • Bank-reported rejection AC04 • Source field references • No automatic retry • Human verification',2.04,6.18,10.28,.29,12.3,C.navy,true);
 small(s,'AC04 is what the bank reported, not independent proof that an account is actually closed. Correlation checks exact identifiers.',.68,6.74,11.85,.24);
}
// Slide 6 — security risk transparent.
{
 const s=pptx.addSlide();section(s,6,'security & risk','Read-only lowers execution risk. It does not mean zero risk.','The highest-value design choice is evidence and access governance — with explicit residual risk owners.');
 const headY=1.99;rect(s,.65,headY,12.05,.42,C.navy,C.navy);text(s,'RISK / FAILURE MODE',.86,2.11,3.17,.18,11,C.white,true);text(s,'CONTROL IN PROTOTYPE OR TARGET DESIGN',4.12,2.11,6.00,.18,11,C.white,true);text(s,'STATE',10.88,2.11,1.34,.18,11,C.white,true);
 const rows=[
 ['Unsafe payment resubmission','No mutation tools; return “no automatic retry”; human decision','TODAY'],
 ['Wrong or invented explanation','Exact MsgId + E2E/UETR correlation; unknown codes never guessed','TODAY'],
 ['Malicious message text / XML','Untrusted labels, injection flags, DTD/XXE and size constraints','TODAY'],
 ['PII leakage into models or logs','Mask/tokenize data; enforce retention and approved model boundary','TARGET'],
 ['Unauthorized bank data access','Bank-controlled OIDC, scoped identity, RBAC and audit','TARGET'],
 ['New scheme/version or partial evidence','Versioned official rules; provenance and safe escalation','GAP']
 ];
 rows.forEach((a,i)=>{let y=2.45+i*.55;rect(s,.65,y,12.05,.51,i%2?C.white:C.pale,i%2?C.white:C.line,.04,.45);text(s,a[0],.85,y+.11,3.08,.29,11.6,C.navy,true);text(s,a[1],4.12,y+.09,6.21,.32,11.0,C.steel);label(s,a[2],10.92,y+.105,1.23,a[2]==='TODAY'?'teal':a[2]==='TARGET'?'amber':'red')});
 rect(s,.65,5.99,12.05,.61,C.redBg,'E7BCBD');text(s,'RESIDUAL RISK',.87,6.20,1.60,.18,11.3,C.red,true);text(s,'Hallucinated synthesis, misconfiguration, PII exposure and false reassurance still require model testing, review and audit.',2.53,6.17,9.86,.28,11.7,C.navy,true);
 small(s,'Never claim “risk-free” or “safe for banking” solely because a tool is read-only. Production deployment requires control testing and bank approval.',.67,6.73,11.95,.28);
}
// Slide 7 — value proposition and proof plan.
{
 const s=pptx.addSlide();section(s,7,'value & investment decision','Prove measurable investigation value — then scale responsibly','The differentiator is explainable exception handling across systems, not another XML parser or the MCP protocol itself.');
 heading(s,'MEASURES THAT MATTER — PILOT SCORECARD',.67,1.93,7.20);
 const rows=[
 ['Investigation handling time','Baseline vs assisted median time'],
 ['Evidence traceability','% of conclusions linked to source fields'],
 ['Case interpretation accuracy','Expert-reviewed correct root-cause attribution'],
 ['Safety / false confidence','Unsupported conclusions, unsafe actions and PII escapes'],
 ['Operational fit','Analyst acceptance and escalation quality']
 ];
 rows.forEach((r,i)=>{const y=2.34+i*.55;rect(s,.67,y,7.31,.50,i%2?C.white:C.pale,C.line,.03,.45);text(s,r[0],.82,y+.10,3.12,.30,12.5,C.navy,true);text(s,r[1],4.00,y+.11,3.77,.28,11.0,C.steel)});
 rect(s,8.23,1.98,4.43,3.25,C.mint,C.mintLine);label(s,'SUCCESS CRITERIA',8.44,2.19,2.10,'teal');text(s,'Evidence before speed',8.46,2.73,3.97,.39,19.1,C.navy,true);text(s,'Demonstrate reliable matching, correct caveats and safe escalation on a reviewed case set before making ROI claims.',8.46,3.29,3.80,1.15,13.1,C.ink);text(s,'No production KPI proven yet.',8.46,4.78,3.77,.23,11.8,C.darkTeal,true);
 heading(s,'RECOMMENDED DELIVERY GATES',.67,5.49,7.3);
 const gates=[['01','Local synthetic proof','CURRENT'],['02','Bank-approved read adapters','NEXT'],['03','Measured controlled pilot','THEN']];
 gates.forEach((g,i)=>{const x=.67+i*4.09;rect(s,x,5.88,3.88,.72,i===0?C.mint:C.pale,i===0?C.mintLine:C.line);text(s,g[0],x+.12,6.11,.35,.24,13.7,i===0?C.darkTeal:C.grey,true);text(s,g[1],x+.55,6.08,3.17,.25,12.1,C.navy,true);});
 small(s,'Executive decision: fund a small evidence-based pilot; do not fund a production payment-action agent until data access, scheme rules and safety gates pass.',.67,6.76,12.0,.28);
}

pptx.writeFile({fileName: process.env.OUTPUT_PPTX || 'ISO20022_Payment_Intelligence_Executive_Overview.pptx'});