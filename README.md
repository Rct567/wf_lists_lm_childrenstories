# Word frequency lists based on AI generated children's stories

This repository contains **word frequency lists** based on AI generated children's stories, and the code to generate them.

## How to use

- Create a .env file based on the .env.example file.
- (Optional) Run `generate_titles.py` to generate titles for the stories.
- Run `generate_stories.py` to generate the stories.
- (Optional) Download [stories.zip](https://github.com/Rct567/wf_lists_lm_childrenstories/releases) to get the generated stories currently used.
- Run `generate_wf_lists.py` to generate the word frequencies lists.

## Word frequency lists overview

| Language | Word count | Story count |
| --- | --- | --- |
| [English](wf_lists/wf_list_en.csv) | 23,486 | 4,281 |
| [Chinese](wf_lists/wf_list_zh.csv) | 27,833 | 4,006 |
| [Spanish](wf_lists/wf_list_es.csv) | 28,031 | 3,995 |
| [Russian](wf_lists/wf_list_ru.csv) | 52,199 | 3,986 |
| [Japanese](wf_lists/wf_list_ja.csv) | 16,594 | 3,980 |
| [Arabic](wf_lists/wf_list_ar.csv) | 70,430 | 3,863 |
| [German](wf_lists/wf_list_de.csv) | 29,899 | 3,558 |
| [Italian](wf_lists/wf_list_it.csv) | 29,516 | 3,557 |
| [Portuguese (Portugal)](wf_lists/wf_list_pt.csv) | 27,791 | 3,550 |
| [French](wf_lists/wf_list_fr.csv) | 29,191 | 3,544 |
| [Dutch](wf_lists/wf_list_nl.csv) | 22,671 | 3,279 |
| [Persian](wf_lists/wf_list_fa.csv) | 15,229 | 2,581 |
| [Greek (Modern)](wf_lists/wf_list_el.csv) | 24,608 | 2,580 |
| [Polish](wf_lists/wf_list_pl.csv) | 42,078 | 2,580 |
| [Portuguese (Brazil)](wf_lists/wf_list_pt_br.csv) | 22,144 | 2,580 |
| [Danish](wf_lists/wf_list_da.csv) | 20,077 | 2,579 |
| [Swedish](wf_lists/wf_list_sv.csv) | 20,540 | 2,577 |
| [Indonesian](wf_lists/wf_list_id.csv) | 12,314 | 2,576 |
| [Vietnamese](wf_lists/wf_list_vi.csv) | 4,404 | 2,576 |
| [Hungarian](wf_lists/wf_list_hu.csv) | 46,931 | 2,573 |
| [Korean](wf_lists/wf_list_ko.csv) | 45,581 | 2,561 |
| [Thai](wf_lists/wf_list_th.csv) | 10,652 | 2,555 |
| [Turkish](wf_lists/wf_list_tr.csv) | 41,352 | 2,552 |
| [Finnish](wf_lists/wf_list_fi.csv) | 41,768 | 2,540 |
| [Norwegian](wf_lists/wf_list_no.csv) | 18,810 | 2,414 |
| [Hebrew](wf_lists/wf_list_he.csv) | 31,087 | 2,401 |
| [Icelandic](wf_lists/wf_list_is.csv) | 28,583 | 2,400 |
| [Catalan](wf_lists/wf_list_ca.csv) | 23,494 | 2,398 |
| [Latvian](wf_lists/wf_list_lv.csv) | 34,915 | 2,382 |
| [Galician](wf_lists/wf_list_gl.csv) | 25,793 | 2,241 |
| [Bulgarian](wf_lists/wf_list_bg.csv) | 30,669 | 2,231 |
| [Macedonian](wf_lists/wf_list_mk.csv) | 27,430 | 2,228 |
| [Bosnian](wf_lists/wf_list_bs.csv) | 34,395 | 2,227 |
| [Albanian](wf_lists/wf_list_sq.csv) | 21,321 | 2,222 |
| [Ukrainian](wf_lists/wf_list_uk.csv) | 37,870 | 2,221 |
| [Croatian](wf_lists/wf_list_hr.csv) | 34,499 | 2,220 |
| [Tagalog](wf_lists/wf_list_tl.csv) | 14,375 | 2,220 |
| [Slovak](wf_lists/wf_list_sk.csv) | 38,508 | 2,217 |
| [Urdu](wf_lists/wf_list_ur.csv) | 9,928 | 2,215 |
| [Romanian](wf_lists/wf_list_ro.csv) | 24,650 | 2,213 |
| [Czech](wf_lists/wf_list_cs.csv) | 39,156 | 2,211 |
| [Lithuanian](wf_lists/wf_list_lt.csv) | 35,926 | 2,211 |
| [Esperanto](wf_lists/wf_list_eo.csv) | 23,467 | 2,208 |
| [Estonian](wf_lists/wf_list_et.csv) | 33,895 | 2,205 |
| [Slovenian](wf_lists/wf_list_sl.csv) | 34,230 | 2,205 |
| [Serbian](wf_lists/wf_list_sr.csv) | 46,368 | 2,200 |
| [Basque](wf_lists/wf_list_eu.csv) | 22,748 | 2,188 |
| [Georgian](wf_lists/wf_list_ka.csv) | 29,548 | 2,187 |
| [Malay](wf_lists/wf_list_ms.csv) | 12,017 | 2,160 |
| [Hindi](wf_lists/wf_list_hi.csv) | 1,650 | 1,723 |
| [Armenian](wf_lists/wf_list_hy.csv) | 18,166 | 1,719 |
| [Malayalam](wf_lists/wf_list_ml.csv) | 2,609 | 1,555 |
| [Afrikaans](wf_lists/wf_list_af.csv) | 12,427 | 1,553 |
| [Bengali (Bangla script)](wf_lists/wf_list_bn.csv) | 2,064 | 1,546 |
| [Breton](wf_lists/wf_list_br.csv) | 15,167 | 1,512 |
| [Telugu](wf_lists/wf_list_te.csv) | 1,965 | 1,487 |
| [Sinhala](wf_lists/wf_list_si.csv) | 2,606 | 1,483 |
| [Tamil](wf_lists/wf_list_ta.csv) | 1,312 | 1,483 |
| [Kazakh](wf_lists/wf_list_kk.csv) | 22,017 | 1,477 |
| [Welsh](wf_lists/wf_list_cy.csv) | 12,348 | 1,242 |
| [Norwegian Nynorsk](wf_lists/wf_list_nn.csv) | 13,376 | 1,240 |
| [Khmer](wf_lists/wf_list_km.csv) | 5,210 | 1,238 |
| [Western Frisian](wf_lists/wf_list_fy.csv) | 12,359 | 1,072 |
| [Romansh](wf_lists/wf_list_rm.csv) | 21,714 | 1,068 |
| [Punjabi](wf_lists/wf_list_pa.csv) | 1,437 | 1,067 |
| [Belarusian](wf_lists/wf_list_be.csv) | 22,557 | 1,065 |
| [Amharic](wf_lists/wf_list_am.csv) | 19,148 | 1,058 |
| [Uighur](wf_lists/wf_list_ug.csv) | 17,901 | 1,058 |
| [Nepali](wf_lists/wf_list_ne.csv) | 1,999 | 1,051 |
| [Yiddish (Hebrew script)](wf_lists/wf_list_yi.csv) | 10,997 | 1,051 |
| [Tibetan](wf_lists/wf_list_bo.csv) | 7,846 | 1,048 |
| [Sundanese](wf_lists/wf_list_su.csv) | 10,316 | 1,047 |
| [Haitian](wf_lists/wf_list_ht.csv) | 4,064 | 1,046 |
| [Mongolian](wf_lists/wf_list_mn.csv) | 15,009 | 1,033 |
| [Latin](wf_lists/wf_list_la.csv) | 17,396 | 1,029 |
| [Lao](wf_lists/wf_list_lo.csv) | 6,859 | 1,022 |
| [Somali](wf_lists/wf_list_so.csv) | 15,935 | 1,005 |
| [Uzbek](wf_lists/wf_list_uz.csv) | 18,189 | 1,005 |
| [Scottish Gaelic](wf_lists/wf_list_gd.csv) | 7,734 | 1,000 |
| [Irish](wf_lists/wf_list_ga.csv) | 9,435 | 992 |
| [Zulu](wf_lists/wf_list_zu.csv) | 27,775 | 976 |
| [Kongo](wf_lists/wf_list_kg.csv) | 11,939 | 952 |
| [Old Church Slavonic](wf_lists/wf_list_cu.csv) | 24,402 | 948 |
| [Tatar](wf_lists/wf_list_tt.csv) | 14,230 | 933 |
| [Tajik](wf_lists/wf_list_tg.csv) | 13,165 | 932 |
| [Javanese](wf_lists/wf_list_jv.csv) | 9,374 | 930 |
| [Swahili](wf_lists/wf_list_sw.csv) | 11,316 | 928 |
| [Chechen](wf_lists/wf_list_ce.csv) | 13,143 | 885 |
| [Malagasy](wf_lists/wf_list_mg.csv) | 8,518 | 866 |