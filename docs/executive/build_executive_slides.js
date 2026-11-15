/**
 * Payment Evidence Intelligence | Executive Architecture and Guardrails
 * 11-slide, native/editable PowerPoint. No external images needed.
 * Run: node docs/executive/build_executive_slides.js
 */
const pptxgen=require('pptxgenjs');
const pptx=new pptxgen(); pptx.layout='LAYOUT_WIDE';
pptx.author='Payment Evidence Intelligence Architecture';
pptx.subject='Executive investment narrative, high-level architecture, MCP tools, trust boundaries, guardrails and risk';
pptx.title='PEI | Payment Evidence Intelligence — Executive Architecture and Guardrails';
pptx.company='ISO 20022 MCP Project'; pptx.lang='en-GB';
pptx.theme={headFontFace:'Aptos Display',bodyFontFace:'Aptos',lang:'en-GB'};
const W=13.333, H=7.5, T=pptx.ShapeType;
const C={navy:'102840',dark:'17334D',ink:'1B344E',steel:'405971',muted:'5C7184',subtle:'718599',teal:'087D83',deepTeal:'08696D',mint:'E9F6F2',mintLine:'B5DED1',blue:'EBF3FA',blueLine:'CCDDE9',purple:'ECEAF8',purpleLine:'CFC7EA',amber:'A26919',sand:'FFF3E0',sandLine:'EDD7AE',red:'AE4347',redBg:'FCEDEE',redLine:'E9C0C2',green:'236E57',greenBg:'E6F5EC',white:'FFFFFF',pale:'F7F9FB',line:'D9E3E9',slate:'31465B'};
function txt(sl,s,x,y,w,h,size=14,color=C.ink,bold=false,extra={}){sl.addText(s,{x,y,w,h,fontFace:'Aptos',fontSize:size,color,bold,margin:0,breakLine:false,fit:'shrink',valign:'mid',...extra});}
function box(sl,x,y,w,h,fill=C.white,stroke=C.line,r=.13,thick=1){sl.addShape(T.roundRect,{x,y,w,h,radius:r,rectRadius:r,fill:{color:fill},line:{color:stroke,width:thick}});}
function line(sl,x1,y1,x2,y2,color=C.line,thick=1,dashed=false){sl.addShape(T.line,{x:x1,y:y1,w:x2-x1,h:y2-y1,line:{color,width:thick,dashType:dashed?'dash':'solid'}});}
function arrow(sl,x1,y1,x2,y2,color=C.teal,thick=1.7,dashed=false){sl.addShape(T.line,{x:x1,y:y1,w:x2-x1,h:y2-y1,line:{color,width:thick,dashType:dashed?'dash':'solid',endArrowType:'triangle'}});}
function pill(sl,s,x,y,w,kind='teal') {const a=kind==='amber'?[C.sand,C.amber,C.sandLine]:kind==='red'?[C.redBg,C.red,C.redLine]:kind==='grey'?[C.pale,C.muted,C.line]:kind==='purple'?[C.purple,C.dark,C.purpleLine]:kind==='blue'?[C.blue,C.ink,C.blueLine]:[C.mint,C.deepTeal,C.mintLine];box(sl,x,y,w,.30,a[0],a[2],.12,.8);txt(sl,s,x+.06,y+.068,w-.12,.17,9.1,a[1],true,{align:'center'});}
function dot(sl,x,y,color=C.teal,r=.09){sl.addShape(T.ellipse,{x,y,w:r,h:r,line:{color},fill:{color}});}
function hdr(sl,n,tag,title,subtitle) {sl.background={color:C.white};sl.addShape(T.rect,{x:0,y:0,w:W,h:.10,fill:{color:C.teal},line:{color:C.teal}});txt(sl,`PEI  /  ${tag.toUpperCase()}`,.55,.30,11,.22,9.8,C.deepTeal,true,{charSpacing:1.0});txt(sl,title,.56,.67,12.18,.55,25,C.navy,true);txt(sl,subtitle,.56,1.26,12.18,.46,12.1,C.muted);line(sl,.56,7.14,12.79,7.14,C.line,.85);txt(sl,'PAYMENT EVIDENCE INTELLIGENCE   |   EXECUTIVE ARCHITECTURE   |   CONCEPT + CURRENT SCOPE',.56,7.20,11.49,.18,8.0,C.subtle);txt(sl,`${n} / 11`,12.04,7.20,.73,.18,8.9,C.subtle,true,{align:'right'});}
function card(sl,x,y,w,h,title,body,opt={}){let {fill=C.pale,stroke=C.line,titleSize=15,bodySize=11.2}=opt;box(sl,x,y,w,h,fill,stroke);txt(sl,title,x+.17,y+.18,w-.34,.35,titleSize,C.navy,true);txt(sl,body,x+.17,y+.61,w-.35,h-.78,bodySize,C.steel);}
function titleSmall(sl,s,x,y,w){txt(sl,s,x,y,w,.24,11,C.deepTeal,true,{charSpacing:.65});}
function lineItem(sl,s,x,y,w,color=C.steel,size=11.5){dot(sl,x,y+.13,C.teal,.08);txt(sl,s,x+.17,y,w-.17,.40,size,color);}
function status(sl,s,x,y,now=true,w=1.30){pill(sl,s,x,y,w,now?'teal':'amber')}

// 1 / executive thesis
{
 const s=pptx.addSlide();s.background={color:C.white};s.addShape(T.rect,{x:0,y:0,w:W,h:3.04,fill:{color:C.navy},line:{color:C.navy}});
 txt(s,'PAYMENT EVIDENCE INTELLIGENCE  /  PEI',.66,.54,9.7,.27,11,'61D6CF',true,{charSpacing:1.4});
 txt(s,'From rejection codes to',.66,1.02,8.7,.56,30,C.white,true);
 txt(s,'defensible decisions.',.66,1.65,8.7,.70,33,'88E0D1',true);
 txt(s,'Evidence-first, AI-assisted payment exception investigation.',.68,2.51,8.99,.29,14,'DCEAF2');
 box(s,9.44,.72,3.28,1.88,C.dark,'46718A');pill(s,'WHAT WE DO NOT BUILD',9.66,.92,2.80,'amber');txt(s,'Not a payment executor',9.67,1.35,2.82,.34,17,C.white,true);txt(s,'No AI-triggered resend, settlement or account changes.',9.68,1.82,2.78,.51,11.3,'E5EDF2');
 const xs=[.64,4.86,9.08];const a=[['PROBLEM','Fragmented payment evidence','Analysts chase pacs.008, pacs.002, rejection codes and system histories.'],['SOLUTION','AI + governed tools + facts','An agent orchestrates; deterministic services correlate, validate and cite evidence.'],['VALUE HYPOTHESIS','Less investigation effort','Target faster triage, reproducible explanations and safer escalation.']];
 a.forEach((r,i)=>{const x=xs[i];pill(s,r[0],x,3.49,1.72,i===2?'blue':i===1?'teal':'amber');box(s,x,3.93,3.61,1.87,i===1?C.mint:C.pale,i===1?C.mintLine:C.line);txt(s,r[1],x+.19,4.16,3.23,.45,17,C.navy,true);txt(s,r[2],x+.19,4.78,3.18,.72,12.4,C.steel)});
 box(s,.64,6.08,12.05,.65,C.blue,C.blueLine);txt(s,'EXECUTIVE PROPOSITION',.84,6.29,2.15,.17,11.3,C.navy,true);txt(s,'Build the evidence layer for payment operations—not another standalone XML validator.',3.13,6.23,9.23,.28,13.2,C.ink,true);
 txt(s,'1 / 11',12.07,7.23,.69,.15,8.5,C.subtle,true,{align:'right'});
}
// 2 / traditional vs PEI
{
 const s=pptx.addSlide();hdr(s,2,'why it matters','Traditional workflow vs evidence-led AI investigation','Keep core payment decisions deterministic. Use AI only where questions and investigation paths vary.');
 const xs=[.63,4.77,8.91],labels=[['TRADITIONAL',C.blue,C.blueLine],['AI WITHOUT MCP',C.pale,C.line],['PEI: AI + MCP',C.mint,C.mintLine]];
 labels.forEach((r,i)=>{const x=xs[i];box(s,x,1.98,3.82,3.75,r[1],r[2]);pill(s,r[0],x+.18,2.16,1.72,i===2?'teal':'blue');});
 const cols=[
 ['Scripted investigation','A fixed API validates XML; analysts manually assemble multiple messages, statuses and context.','Best when every workflow is known.'],
 ['Flexible but bespoke','An AI agent chooses questions and calls custom wrappers. Each client needs integration work.','Good flexibility; less portability.'],
 ['Reusable, evidence-first','AI understands intent. MCP discovers tools. Deterministic rules connect facts and preserve source paths.','Best for changing investigation paths.']
 ];
 cols.forEach((a,i)=>{let x=xs[i];txt(s,a[0],x+.18,2.74,3.40,.48,18,C.navy,true);txt(s,a[1],x+.18,3.39,3.40,1.15,12.35,C.steel);line(s,x+.18,4.80,x+3.62,4.80,C.line,1);txt(s,a[2],x+.18,5.01,3.36,.47,11.6,i===2?C.deepTeal:C.muted,true)});
 box(s,.63,5.98,12.10,.66,C.blue,C.blueLine);txt(s,'WHO DOES WHAT?',.84,6.19,1.95,.22,11.7,C.ink,true);txt(s,'AI = reasoning & explanation   |   MCP = tool contract   |   Bank services = facts, validation & authorization',2.94,6.17,9.47,.28,12.7,C.ink,true);
 txt(s,'MCP itself does not increase payment correctness; it standardizes AI access to tools.',.64,6.75,11.96,.22,10.2,C.subtle);
}
// 3 / differentiation
{
 const s=pptx.addSlide();hdr(s,3,'differentiation','What is genuinely intelligent?','A closed-form validator returns errors. PEI investigates evidence, explains uncertainty and governs next actions.');
 const a=[
  ['01','CORRELATE','Exact pacs.008↔pacs.002 message and transaction identifiers.','IMPLEMENTED'],
  ['02','TRACE','Evidence ledger links findings to message fields.','IMPLEMENTED'],
  ['03','KNOW LIMITS','Unknown reason codes stay unknown; bank-reported ≠ independently proven.','IMPLEMENTED'],
  ['04','ORCHESTRATE','AI selects tools for varied analyst requests.','CLIENT ROLE'],
  ['05','EXPAND','Payment hub, ledger, scheme rules and history integration.','TARGET']
 ];
 a.forEach((q,i)=>{const x=.61+(i%3)*4.21,y=2.02+Math.floor(i/3)*1.68,w=4.01;box(s,x,y,w,1.52,i===2?C.mint:C.pale,i===2?C.mintLine:C.line);txt(s,q[0],x+.17,y+.18,.40,.26,17,i===2?C.deepTeal:C.subtle,true);pill(s,q[3],x+2.40,y+.14,1.35,q[3]==='TARGET'?'amber':q[3]==='CLIENT ROLE'?'blue':'teal');txt(s,q[1],x+.66,y+.19,1.68,.27,15,C.navy,true);txt(s,q[2],x+.18,y+.65,w-.38,.69,11.9,C.steel)});
 box(s,9.03,3.69,3.99,1.51,C.sand,C.sandLine);txt(s,'Illustrative finding',9.23,3.89,3.49,.31,15.5,C.navy,true);txt(s,'“Bank reported RJCT / AC04. IDs match. Account closure is not independently verified; do not auto-retry.”',9.23,4.29,3.55,.72,12.1,C.ink);
 box(s,.62,5.74,12.10,.78,C.blue,C.blueLine);txt(s,'Differentiation is the investigation workflow + evidence quality—not using Python, MCP, or Glama.',.85,5.92,11.67,.34,14.3,C.ink,true);
 txt(s,'A live multi-system investigation has not been delivered; only supplied XML correlation is currently implemented.',.64,6.74,11.94,.22,10.3,C.subtle);
}
// 4 / high-level reference architecture
{
 const s=pptx.addSlide();hdr(s,4,'high-level architecture','Target architecture | AI is outside the banking trust boundary','A single ISO 20022 core can serve both conventional REST applications and an MCP-enabled operations copilot.');
 titleSmall(s,'CHANNELS',.65,1.88,2.20);
 box(s,.64,2.20,3.15,.67,C.blue,C.blueLine);txt(s,'Banking portal / REST client',.79,2.36,2.89,.29,14,C.navy,true,{align:'center'});
 box(s,4.08,2.20,3.20,.67,C.mint,C.mintLine);txt(s,'Payment Ops AI Copilot',4.23,2.36,2.90,.29,14,C.navy,true,{align:'center'});
 arrow(s,2.20,2.90,2.20,3.17,C.teal,1.8);arrow(s,5.65,2.90,5.65,3.17,C.teal,1.8);
 titleSmall(s,'GOVERNED ACCESS',.65,3.08,2.55);
 box(s,.65,3.43,6.64,.76,C.sand,C.sandLine);txt(s,'Policy gateway  /  OIDC  /  RBAC  /  redaction  /  audit  /  rate limits',.82,3.59,6.29,.37,13.2,C.navy,true,{align:'center'});pill(s,'TARGET',6.18,3.08,1.05,'amber');
 arrow(s,4.02,4.24,4.02,4.56,C.teal,1.8);
 titleSmall(s,'DETERMINISTIC FINANCIAL SERVICES',.65,4.48,5.12);
 box(s,.65,4.82,6.64,1.04,C.mint,C.mintLine);txt(s,'ISO 20022 evidence core',.88,5.00,5.99,.30,17,C.navy,true);txt(s,'Parsing · validation · exact correlation · code sets · safe findings',.88,5.46,5.98,.24,11.7,C.steel);pill(s,'IMPLEMENTED',5.97,4.49,1.32,'teal');
 line(s,7.29,5.30,7.52,5.30,C.amber,1.8,true);line(s,7.52,5.30,7.52,2.77,C.amber,1.8,true);arrow(s,7.52,2.77,7.76,2.77,C.amber,1.8,true);
 titleSmall(s,'BANK-OWNED ADAPTER / DATA PLANE',7.77,1.89,4.93);
 box(s,7.78,2.20,4.90,.95,C.sand,C.sandLine);txt(s,'Read-only anti-corruption layer',7.98,2.38,4.48,.28,15,C.navy,true);txt(s,'Contracts, mapping, access checks, source timestamps',7.98,2.78,4.48,.21,11.0,C.steel);pill(s,'TARGET',11.41,1.88,1.25,'amber');
 arrow(s,10.20,3.19,10.20,3.51,C.amber,1.8,true);
 [['Payment hub','pacs.008 / pacs.002'],['Core banking','Account / ledger status'],['MQ / SOAP / Batch','Legacy read interfaces'],['Archive / rules','History / official rules']].forEach((a,i)=>{let x=7.78+(i%2)*2.52,y=3.58+Math.floor(i/2)*1.09;box(s,x,y,2.38,.91,C.pale,C.line);txt(s,a[0],x+.14,y+.15,2.10,.25,13.1,C.navy,true);txt(s,a[1],x+.14,y+.51,2.11,.22,10.7,C.steel)});
 box(s,.65,6.23,12.03,.48,C.redBg,C.redLine);txt(s,'NON-NEGOTIABLE:  no direct LLM-to-core connection, no write scope, no AI-triggered resubmission or settlement.',.82,6.32,11.67,.29,12.5,C.red,true,{align:'center'});
 txt(s,'Glama is optional discovery/publishing infrastructure; it is not required in the transaction path. Arrows to banking systems are target architecture.',.67,6.77,11.97,.20,9.9,C.subtle);
}
// 5 / guardrail architecture
{
 const s=pptx.addSlide();hdr(s,5,'guardrails & control plane','Guardrails must be enforced at each trust boundary','A prompt saying “be safe” is not a control. Policies, data filters, authorization and evidence checks must be deterministic.');
 const rows=[
  ['1','IDENTITY','Authenticate analyst and service; authorize each bank evidence read.','TARGET'],
  ['2','DATA','Minimize/tokenize PII; reject secrets and control sensitive data egress.','TARGET'],
  ['3','AGENT','Mark suspicious remittance as untrusted; enforce isolation in target.','PARTIAL'],
  ['4','MCP TOOLS','Allowlist read-only tools; validate schemas, limits, timeouts and scopes.','PARTIAL'],
  ['5','FINANCIAL TRUTH','Exact identifier matching, approved XSD/rules, provenance and uncertainty.','PARTIAL'],
  ['6','ACTION','No payment writes exposed; recommend human review for remediation.','CURRENT'],
  ['7','ASSURANCE','Immutable audit, red-team tests, monitoring, kill switch and owners.','TARGET']
 ];
 rows.forEach((r,i)=>{const x=.63,y=1.97+i*.595;box(s,x,y,12.08,.53,i%2?C.white:C.pale,C.line,.04,.6);box(s,x+.12,y+.105,.30,.30,C.navy,C.navy,.05);txt(s,r[0],x+.12,y+.18,.30,.12,10,C.white,true,{align:'center'});txt(s,r[1],x+.54,y+.12,2.10,.26,12.3,C.navy,true);txt(s,r[2],x+2.75,y+.11,7.43,.30,11.55,C.steel);pill(s,r[3],x+10.47,y+.115,1.38,r[3]==='CURRENT'?'teal':r[3]==='PARTIAL'?'blue':'amber');});
 box(s,.64,6.37,12.05,.44,C.redBg,C.redLine);txt(s,'FAIL CLOSED if identity, correlation, schema obligations or evidence are insufficient. Never infer bank-authorized action.',.86,6.48,11.62,.20,11.9,C.red,true,{align:'center'});
 txt(s,'“Partial” means one or more protections are coded, but a production enforcement plane is not yet in place.',.66,6.84,11.88,.20,10.0,C.subtle);
}
// 6 / tool inventory
{
 const s=pptx.addSlide();hdr(s,6,'tool catalogue','What AI can call today—and what still needs banking integration','Six implemented read-only tools have explicit scope. Bank data retrieval and automated remediation are not available.');
 const items=[
 ['parse_message','Extract IDs, parties and message fields.'],
 ['validate_message','Check business rules; optional XSD and security outcomes.'],
 ['investigate_payment','Correlate supplied pacs.008 and pacs.002; return evidence.'],
 ['lookup_code','Look up known status and reason codes.'],
 ['explain_message','Deterministic payment summary.'],
 ['generate_test_message','Synthetic pacs.008 / pacs.002 fixtures.']
 ];
 titleSmall(s,'IMPLEMENTED IN PYTHON MCP SERVER',.65,1.93,7.8);
 items.forEach((a,i)=>{let x=.65+(i%2)*4.18,y=2.34+Math.floor(i/2)*1.17;box(s,x,y,4.00,1.01,i===2?C.mint:C.pale,i===2?C.mintLine:C.line);txt(s,a[0],x+.17,y+.16,3.64,.28,14.1,C.navy,true);txt(s,a[1],x+.17,y+.53,3.64,.30,11.0,C.steel)});
 box(s,9.25,1.95,3.44,3.96,C.sand,C.sandLine);pill(s,'PROPOSED / NOT IMPLEMENTED',9.46,2.16,2.98,'amber');txt(s,'Future bank tools',9.47,2.65,2.96,.36,17.2,C.navy,true);
 ['get_payment_evidence','get_payment_status','get_scheme_rules','check_duplicate_payment','simulate_repair'].forEach((name,i)=>{dot(s,9.50,3.27+i*.43,C.amber,.09);txt(s,name,9.67,3.16+i*.43,2.80,.30,11.7,C.ink,true)});
 box(s,.65,6.09,12.04,.60,C.blue,C.blueLine);txt(s,'Agent may call:',.83,6.27,1.60,.21,12.7,C.navy,true);txt(s,'approved read-only tools   |   Agent may not call: payment initiation, account updates, refunds or settlement',2.50,6.25,9.94,.27,12.1,C.ink);
 txt(s,'MCP does not make every banking API safe; the gateway and adapters enforce identity, data minimization, permissions and logging.',.66,6.80,12.03,.22,9.8,C.subtle);
}
// 7 / sequence
{
 const s=pptx.addSlide();hdr(s,7,'investigation sequence','Happy path | “Why was payment REF123 rejected?”','Existing local flow: supplied synthetic messages. Retrieval from bank systems is a separate target integration.');
 const lanes=[{x:.65,w:2.0,l:'ANALYST'},{x:2.93,w:2.20,l:'AI CLIENT'},{x:5.38,w:2.25,l:'MCP SERVER'},{x:7.88,w:2.20,l:'EVIDENCE ENGINE'}];
 lanes.forEach(a=>{box(s,a.x,1.96,a.w,.43,a.l==='MCP SERVER'?C.mint:C.blue,a.l==='MCP SERVER'?C.mintLine:C.blueLine);txt(s,a.l,a.x+.05,2.09,a.w-.10,.18,10.4,C.navy,true,{align:'center'});line(s,a.x+a.w/2,2.45,a.x+a.w/2,5.93,C.line,.75,true)});
 const steps=[
  [2.76,1.64,3.99,'1 Ask about REF123'],
  [3.26,4.02,6.49,'2 initialize / tools/list'],
  [3.76,4.02,6.49,'3 validate_message(xml)'],
  [4.26,6.52,8.96,'4 investigate_payment(xml×2)'],
  [4.76,8.96,6.52,'5 exact correlation + AC04'],
  [5.26,6.49,4.02,'6 evidence, limits, no retry'],
  [5.76,3.99,1.64,'7 human-reviewed explanation']
 ];
 steps.forEach((r,i)=>{arrow(s,r[1],r[0],r[2],r[0],i===4?C.teal:C.dark,1.45);txt(s,r[3],Math.min(r[1],r[2]),r[0]-.29,Math.abs(r[2]-r[1]),.24,10.1,C.navy,true,{align:'center'})});
 box(s,10.34,1.97,2.35,3.97,C.pale,C.line);pill(s,'SYNTHETIC PAIR',10.52,2.19,1.96,'blue');txt(s,'pacs.008',10.55,2.71,1.89,.29,13.7,C.navy,true);txt(s,'MsgId = M-123\nE2E = E-123',10.54,3.10,1.91,.59,11.4,C.steel);line(s,10.52,3.83,12.49,3.83,C.line,1);txt(s,'pacs.002',10.55,4.03,1.90,.29,13.7,C.navy,true);txt(s,'OrgnlMsgId = M-123\nE2E = E-123\nRJCT  /  AC04',10.54,4.44,1.90,.90,11.0,C.steel);
 box(s,.65,6.13,12.04,.59,C.mint,C.mintLine);txt(s,'OUTPUT',.86,6.32,1.01,.18,11.1,C.deepTeal,true);txt(s,'Matched IDs  •  reported rejection  •  field-level evidence  •  unknowns  •  operator escalation',1.95,6.28,10.38,.28,12.2,C.navy,true);
 txt(s,'A reported AC04 code is evidence of the bank response, not direct verification of account status or permission to retry.',.66,6.81,12.04,.20,10.0,C.subtle);
}
// 8 / integration patterns
{
 const s=pptx.addSlide();hdr(s,8,'core + legacy integration','Connect through bank-owned adapters—not through the LLM','Existing adapters are interfaces only. A bank must provide the integration implementation, identity and authoritative data access.');
 const patterns=[
 ['REST / z/OS Connect','Modern core APIs or CICS/IMS via bank API management.','Read-only OAuth/mTLS; RBAC; correlation IDs.'],
 ['IBM MQ','Request/reply via ESB or payment event stream.','MQ identity; DLQ, TTL, idempotency, audit.'],
 ['SOAP / ESB','Existing services wrapped with approved contracts.','WS-Security/mTLS; mapping and payload limits.'],
 ['Batch / Archive','Controlled extract from files, archive or CDC.','Freshness markers; least data; signed lineage.']
 ];
 patterns.forEach((p,i)=>{let x=.64+(i%2)*6.14,y=2.05+Math.floor(i/2)*1.66;box(s,x,y,5.92,1.46,i===0?C.mint:C.pale,i===0?C.mintLine:C.line);pill(s,`PATTERN ${i+1}`,x+.15,y+.12,1.25,i===0?'teal':'blue');txt(s,p[0],x+1.60,y+.16,4.10,.27,15.8,C.navy,true);txt(s,p[1],x+.19,y+.58,5.49,.34,11.7,C.steel);txt(s,p[2],x+.19,y+1.05,5.49,.23,11,C.deepTeal,true)});
 box(s,.65,5.57,12.02,.82,C.sand,C.sandLine);txt(s,'Bank boundary',.85,5.75,1.72,.25,14.4,C.navy,true);txt(s,'AI → MCP gateway → authorization + PII policy → read adapter → core/payment hub → normalized evidence',2.52,5.73,9.88,.31,12.5,C.ink,true);
 txt(s,'DO NOT expose mainframe credentials, raw unrestricted ledgers, broad MQ topics or write methods to the AI/MCP surface.',.67,6.58,11.97,.30,11.4,C.red,true);
}
// 9 / risk and controls, avoid "no risk"
{
 const s=pptx.addSlide();hdr(s,9,'threats & residual risk','Security posture | controlled risk, not “no risk”','Read-only prevents the agent from directly changing a payment; privacy, false confidence and unauthorized reads remain major risks.');
 box(s,.65,1.96,12.04,.43,C.navy,C.navy);txt(s,'RISK',.85,2.07,3.06,.22,11.3,C.white,true);txt(s,'CONTROL / MITIGATION',3.82,2.07,6.45,.22,11.3,C.white,true);txt(s,'STATUS',10.68,2.07,1.52,.22,11.3,C.white,true);
 const data=[
 ['Wrong correlation / wrong conclusion','Exact original message ID + transaction IDs; explain source and uncertainty.','PARTIAL'],
 ['Untrusted XML or prompt injection','Safe parser; XXE restrictions; suspicious text marked untrusted.','IMPLEMENTED'],
 ['Unauthorized bank evidence access','OIDC/RBAC; scoped service identity; request-by-request access checks.','TARGET'],
 ['PII leakage to model or logs','Tokenization, field allowlists, approved model boundary, retention.','TARGET'],
 ['Misleading scheme interpretation','Versioned official XSD / SEPA / CBPR+ rules; expert exception review.','TARGET'],
 ['Automated repair / incorrect retry','No write tools, no auto-retry; human-controlled payment action elsewhere.','IMPLEMENTED']
 ];
 data.forEach((r,i)=>{let y=2.43+i*.566;box(s,.65,y,12.04,.54,i%2?C.white:C.pale,C.line,.03,.65);txt(s,r[0],.84,y+.08,2.84,.37,11.9,C.navy,true);txt(s,r[1],3.82,y+.09,6.57,.36,11.1,C.steel);pill(s,r[2],10.73,y+.115,1.56,r[2]==='TARGET'?'amber':r[2]==='PARTIAL'?'blue':'teal')});
 box(s,.65,5.99,12.04,.65,C.redBg,C.redLine);txt(s,'RESIDUAL RISK',.84,6.20,1.70,.19,11.9,C.red,true);txt(s,'An AI answer can still be wrong. Source evidence, explicit uncertainty, red-team tests and human governance are mandatory.',2.57,6.15,9.82,.33,11.9,C.navy,true);
 txt(s,'Pilot approval must assess data protection, architecture, model risk and bank-specific regulatory obligations.',.67,6.79,11.93,.24,10.2,C.subtle);
}
// 10 / pilot evidence
{
 const s=pptx.addSlide();hdr(s,10,'measurable value','Investment case | proof by controlled benchmark, not claims','Demonstrate value against today’s manual / API-only workflow on a blind, bank-approved case set.');
 const x=[.66,4.78,8.90];
 [['SPEED','Median analyst handling time','Compare start-to-decision timestamps.'],['TRUST','Evidence-linked conclusion rate','Sample correctness and source traceability.'],['SAFETY','Unsupported claims / unsafe actions','Track false attributions, privacy events and retry suggestions.']].forEach((p,i)=>{box(s,x[i],2.04,3.80,2.01,i===1?C.mint:C.pale,i===1?C.mintLine:C.line);pill(s,p[0],x[i]+.17,2.24,1.27,i===1?'teal':'blue');txt(s,p[1],x[i]+.18,2.72,3.40,.58,17,C.navy,true);txt(s,p[2],x[i]+.18,3.47,3.39,.37,11.7,C.steel)});
 box(s,.66,4.31,12.04,1.37,C.blue,C.blueLine);titleSmall(s,'CONTROLLED PILOT DESIGN',.85,4.53,5.14);txt(s,'1   Baseline on the same cases',.86,4.93,3.49,.32,12.3,C.ink,true);txt(s,'2   Blind expert review',4.53,4.93,3.19,.32,12.3,C.ink,true);txt(s,'3   Adversarial / missing-data tests',8.01,4.93,4.31,.32,12.3,C.ink,true);
 box(s,.67,5.90,12.02,.73,C.sand,C.sandLine);txt(s,'INVESTMENT RULE',.85,6.13,1.95,.20,11.7,C.amber,true);txt(s,'Do not claim ROI, investigation accuracy or “AI safety” until measured against predefined acceptance gates.',2.89,6.10,9.43,.31,12.5,C.ink,true);
 txt(s,'Current synthetic fixtures demonstrate tool correctness only. They do not establish production accuracy or business benefit.',.67,6.77,11.93,.22,10.2,C.subtle);
}
// 11 / roadmap & gates
{
 const s=pptx.addSlide();hdr(s,11,'executive decision','Recommended path | prove, secure, integrate, then scale','A small controlled pilot establishes whether PEI has a defensible advantage over traditional integration approaches.');
 const stages=[
  ['GATE 0','WORKING FOUNDATION','Local MCP tool suite; exact message correlation; evidence outputs; synthetic regression.','TODAY'],
  ['GATE 1','CONTROLLED BANK PILOT','Bank-approved data access; PII policy; evidence corpus; review owners and scorecard.','NEXT'],
  ['GATE 2','LEGACY INTEGRATION','Read-only REST/zOS/MQ/SOAP adapters, audit/observability, approved XSD/rules.','TARGET'],
  ['GATE 3','OPERATIONAL SCALE','Performance/SLA, rule version governance, model monitoring and formal change control.','TARGET']
 ];
 stages.forEach((a,i)=>{let x=.61+i*3.11;box(s,x,2.05,2.95,3.12,i===0?C.mint:C.pale,i===0?C.mintLine:C.line);pill(s,a[0],x+.16,2.24,1.28,i===0?'teal':'blue');txt(s,a[1],x+.16,2.76,2.60,.59,15.4,C.navy,true);txt(s,a[2],x+.16,3.51,2.61,1.20,11.9,C.steel);pill(s,a[3],x+.17,4.74,1.35,i===0?'teal':'amber');if(i<3)arrow(s,x+2.98,3.59,x+3.10,3.59,C.teal,1.9)});
 box(s,.64,5.48,12.05,.87,C.navy,C.navy);txt(s,'EXECUTIVE ASK',.85,5.74,2.09,.23,12.5,'8EE0D5',true);txt(s,'Approve a scoped read-only pilot and measure evidence quality, analyst productivity and residual risk.',2.96,5.69,9.42,.37,15.5,C.white,true);
 txt(s,'Not requested: autonomous financial decisions, payment write access, or production approval before bank security and model-risk assessment.',.66,6.61,11.96,.35,11.2,C.red,true);
}

pptx.writeFile({fileName:process.env.OUTPUT_PPTX||'ISO20022_Payment_Intelligence_Executive_Overview.pptx'});