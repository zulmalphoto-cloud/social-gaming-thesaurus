import json
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title='Social Gaming Research Explorer',page_icon='🎮',layout='wide')
st.markdown('''<style>.block-container{padding-top:2rem;max-width:1250px}.stMetric{border:1px solid #e5e7eb;border-radius:12px;padding:12px}.small-note{color:#667085;font-size:0.87rem}</style>''',unsafe_allow_html=True)
DATA=Path(__file__).with_name('studies.json')
studies=json.loads(DATA.read_text(encoding='utf-8'))
COLORS={'Conceptual':'#7555A4','In-person':'#247C70','Digital':'#326D9B','Human-machine':'#A44970','Playfulness':'#AD682F','Context':'#536A38'}
terms={
 'Artificial social entity':('Human-machine','Bot, NPC or AI acting as a teammate, opponent, or social character.'),
 'Asynchronous social gaming':('Digital','Social interaction during games occurring at different times, such as message or photo exchanges.'),
 'Cooperative gameplay':('In-person','Joint activity toward shared goals; possible in-person or online.'),
 'Face-to-face social interaction':('In-person','Verbal and nonverbal exchanges during co-located play.'),
 'Human–machine gameplay':('Human-machine','Playing with or against an automated agent; whether it counts as social varies by framework.'),
 'Intergenerational tele-gaming':('Digital','Remote game-based interaction between different age groups.'),
 'Multiplayer gaming':('Digital','More than one active player; does not itself establish the quality of social interaction.'),
 'Social engagement during gameplay':('In-person','Observable game-related physical, verbal and affective responses.'),
 'Social gaming':('Conceptual','Umbrella term used differently across the literature.'),
 'Social playfulness':('Playfulness','Spontaneous reciprocal play that may not involve formal game rules.'),
 'Social presence':('Conceptual','Experience or structure of being with others in physical or virtual contexts.'),
 'Social outcomes':('Conceptual','Potential consequences such as connectedness or loneliness, distinct from game features.')}

st.title('Social Gaming Research Explorer')
st.caption('CSUN × Johns Hopkins | Working research thesaurus')
st.info('Research status: These are paraphrases from supplied literature summaries, not independently verified extractions from full-text articles. Confirm author/year, wording, instruments, and page numbers before citation.')
tab1,tab2,tab3,tab4=st.tabs(['Study library','Compare studies','A–Z terminology','Add / export'])
with tab1:
 left,right=st.columns([2,1]); q=left.text_input('Search studies and operationalizations',placeholder='Try: chatbot, Go, human, loneliness...'); kinds=right.multiselect('Filter by category',list(COLORS),default=[])
 filtered=[s for s in studies if (not kinds or s['category'] in kinds) and (not q or q.lower() in ' '.join(str(v) for v in s.values()).lower())]
 st.caption(f'{len(filtered)} of {len(studies)} studies')
 for s in filtered:
  with st.expander(f"{s['author']} · {s['title']}"):
   st.markdown(f"<span style='color:{COLORS.get(s['category'],'#555')}'>{s['category']}</span>",unsafe_allow_html=True)
   for label,key in [('Conceptual definition','definition'),('Game / setting','setting'),('Operationalization / evidence','operationalization'),('Outcomes / related measures','outcomes'),('Interpretive note','notes')]:st.markdown(f'**{label}**  \n{s[key]}')
with tab2:
 names=[f"{s['author']} — {s['title']}" for s in studies]
 a,b=st.columns(2); ai=a.selectbox('First study',range(len(studies)),format_func=lambda i:names[i],index=0);bi=b.selectbox('Second study',range(len(studies)),format_func=lambda i:names[i],index=3)
 if ai==bi:st.warning('Choose two different studies to compare.')
 else:
  for label,key in [('Definition','definition'),('Setting','setting'),('Operationalization','operationalization'),('Outcome','outcomes'),('Caveat','notes')]:
   st.subheader(label);c1,c2=st.columns(2);c1.write(studies[ai][key]);c2.write(studies[bi][key])
with tab3:
 termq=st.text_input('Find a term',placeholder='Search the alphabetical index')
 for term,(kind,definition) in sorted(terms.items()):
  if termq.lower() in (term+' '+definition).lower():
   st.markdown(f"<div style='border-left:5px solid {COLORS[kind]};padding:7px 14px;margin:8px 0'><strong>{term}</strong> <small>· {kind}</small><br>{definition}</div>",unsafe_allow_html=True)
 st.caption('This initial index contains 12 terms; it can be expanded as primary articles are reviewed.')
with tab4:
 st.subheader('Add a study during your session')
 with st.form('new_study'):
  author=st.text_input('Authors and year');title=st.text_input('Study title');kind=st.selectbox('Category',list(COLORS));definition=st.text_area('Conceptual definition');oper=st.text_area('Operationalization');setting=st.text_input('Game / setting');outcomes=st.text_input('Outcomes or related measures');notes=st.text_area('Notes / citation verification');submitted=st.form_submit_button('Add to session')
 if 'extra' not in st.session_state:st.session_state.extra=[]
 if submitted:
  if author.strip() and title.strip():
   st.session_state.extra.append(dict(author=author,title=title,category=kind,definition=definition,setting=setting,operationalization=oper,outcomes=outcomes,notes=notes,verified=False));st.success('Added for this session. Export below to preserve it.')
  else:st.error('Author and title are required.')
 all_studies=studies+st.session_state.extra
 st.download_button('Download study database (CSV)',pd.DataFrame(all_studies).to_csv(index=False).encode('utf-8-sig'),'social_gaming_studies.csv','text/csv')
 st.download_button('Download study database (JSON)',json.dumps(all_studies,indent=2,ensure_ascii=False),'studies_updated.json','application/json')
 st.caption('New entries are temporary until exported. To publish them permanently, replace studies.json in your repository with the downloaded JSON file.')
