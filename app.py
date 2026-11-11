import json
from pathlib import Path
import pandas as pd
import streamlit as st
st.set_page_config(page_title='Social Gaming Thesaurus',page_icon='📚',layout='wide')
BASE=Path(__file__).parent
entries=json.loads((BASE/'thesaurus.json').read_text(encoding='utf-8'))
studies=json.loads((BASE/'studies.json').read_text(encoding='utf-8'))
COLORS={'Conceptual':'#7555A4','In-person':'#247C70','Digital':'#326D9B','Human-machine':'#A44970','Playfulness':'#AD682F','Context':'#536A38'}
st.title('Social Gaming Thesaurus')
st.caption('Interactive terminology and study explorer | CSUN × Johns Hopkins research collaboration')
st.warning('Working research compilation: entries and source-to-instrument links come from supplied summaries, not independently verified original publications. Some UF labels may be related phrases rather than true synonyms. Validate before scholarly citation.')
term_tab,study_tab,compare_tab,source_tab,add_tab=st.tabs(['A–Z Thesaurus','Study library','Compare studies','Original source material','Add / export'])
with term_tab:
 st.subheader('Explore all 18 headwords')
 q=st.text_input('Search terms, scope notes, indicators, studies, and synonyms',key='term_search')
 filtered=[e for e in entries if q.lower() in json.dumps(e,ensure_ascii=False).lower()]
 st.caption(f'{len(filtered)} of {len(entries)} headwords')
 for e in sorted(filtered,key=lambda x:x['term'].casefold()):
  with st.expander(e['term']):
   for code,label in [('SN','Scope note / definition'),('UF','Used for / proposed alternative terms'),('BT','Broader terms'),('NT','Narrower terms'),('RT','Related terms'),('OP','Operational indicators'),('IN','Instruments / paradigms'),('CS','Studies / authors')]:
    st.markdown(f'**{code} — {label}**')
    if e[code]:
     for val in e[code]:st.write('• '+val)
    else:st.caption('Not supplied')
   with st.popover('See full original entry'):st.text(e['raw_entry'])
 st.info('A–Z organization does not imply that every source-provided BT/NT/UF relationship has been validated. The original wording is retained for review.')
with study_tab:
 st.subheader('Study summaries')
 q=st.text_input('Search authors, definitions, and operationalizations')
 categories=st.multiselect('Categories',sorted(set(s['category'] for s in studies)))
 subset=[s for s in studies if (not categories or s['category'] in categories) and q.lower() in json.dumps(s,ensure_ascii=False).lower()]
 st.caption(f'{len(subset)} of {len(studies)} detailed study summaries. Additional authors are indexed within thesaurus entries.')
 for s in subset:
  with st.expander(f"{s['author']} — {s['title']}"):
   st.caption(s['category'])
   for label,key in [('Conceptual definition','definition'),('Setting','setting'),('Operationalization','operationalization'),('Outcomes','outcomes'),('Notes','notes')]:st.markdown(f'**{label}:** {s.get(key,"")}')
with compare_tab:
 st.subheader('Compare operationalizations')
 names=[e['term'] for e in sorted(entries,key=lambda x:x['term'].casefold())]
 c1,c2=st.columns(2)
 a=c1.selectbox('First term',names,index=0)
 b=c2.selectbox('Second term',names,index=min(1,len(names)-1))
 ea=next(e for e in entries if e['term']==a);eb=next(e for e in entries if e['term']==b)
 for code,label in [('SN','Scope note'),('BT','Broader'),('NT','Narrower'),('RT','Related'),('OP','Operational indicators'),('IN','Instruments'),('CS','Sources')]:
  st.markdown('#### '+label)
  ca,cb=st.columns(2)
  ca.write('\n\n'.join(ea[code]) or 'Not supplied');cb.write('\n\n'.join(eb[code]) or 'Not supplied')
with source_tab:
 st.subheader('Preserved source materials')
 st.write('Both complete uploaded text compilations are included without deleting overlapping material. The second contains additional discussions of human–machine gaming and earlier study-by-study comparisons.')
 for name,label in [('source_master_thesaurus.txt','Complete 18-headword master thesaurus'),('source_additional_notes.txt','Earlier thesaurus, study summaries, and human–machine notes')]:
  raw=(BASE/name).read_text(encoding='utf-8')
  st.download_button('Download '+label,raw,file_name=name,mime='text/plain',key=name)
  with st.expander('Read '+label):st.text_area(label,raw,height=340,key='view_'+name)
with add_tab:
 st.subheader('Export the full database')
 st.download_button('Download all 18 entries (JSON)',json.dumps(entries,indent=2,ensure_ascii=False),file_name='thesaurus.json',mime='application/json')
 st.download_button('Download all 18 entries (CSV)',pd.DataFrame([{**{'term':e['term']},**{k:' | '.join(e[k]) for k in ['SN','UF','BT','NT','RT','OP','IN','CS']}} for e in entries]).to_csv(index=False).encode('utf-8-sig'),file_name='thesaurus.csv',mime='text/csv')
 st.download_button('Download study summaries (JSON)',json.dumps(studies,indent=2,ensure_ascii=False),file_name='studies.json',mime='application/json')
 st.info('To permanently add or edit entries, update thesaurus.json in GitHub. The public website reads that file on restart/redeploy; edits in a visitor browser are not saved to a shared database.')
