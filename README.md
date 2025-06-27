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
| [English](wf_lists/wf_list_en.csv) | 23,323 | 4,236 |
| [Chinese](wf_lists/wf_list_zh.csv) | 27,633 | 3,963 |
| [Spanish](wf_lists/wf_list_es.csv) | 27,788 | 3,951 |
| [Russian](wf_lists/wf_list_ru.csv) | 51,777 | 3,945 |
| [Japanese](wf_lists/wf_list_ja.csv) | 16,482 | 3,938 |
| [Arabic](wf_lists/wf_list_ar.csv) | 69,450 | 3,820 |
| [German](wf_lists/wf_list_de.csv) | 29,579 | 3,516 |
| [Italian](wf_lists/wf_list_it.csv) | 29,187 | 3,512 |
| [Portuguese (Portugal)](wf_lists/wf_list_pt.csv) | 27,577 | 3,508 |
| [French](wf_lists/wf_list_fr.csv) | 28,915 | 3,504 |
| [Dutch](wf_lists/wf_list_nl.csv) | 22,440 | 3,237 |
| [Danish](wf_lists/wf_list_da.csv) | 19,840 | 2,539 |
| [Persian](wf_lists/wf_list_fa.csv) | 15,067 | 2,538 |
| [Portuguese (Brazil)](wf_lists/wf_list_pt_br.csv) | 21,914 | 2,537 |
| [Greek (Modern)](wf_lists/wf_list_el.csv) | 24,314 | 2,536 |
| [Polish](wf_lists/wf_list_pl.csv) | 41,473 | 2,536 |
| [Swedish](wf_lists/wf_list_sv.csv) | 20,298 | 2,535 |
| [Vietnamese](wf_lists/wf_list_vi.csv) | 4,386 | 2,535 |
| [Indonesian](wf_lists/wf_list_id.csv) | 12,190 | 2,532 |
| [Hungarian](wf_lists/wf_list_hu.csv) | 46,077 | 2,531 |
| [Korean](wf_lists/wf_list_ko.csv) | 44,818 | 2,519 |
| [Thai](wf_lists/wf_list_th.csv) | 10,518 | 2,513 |
| [Turkish](wf_lists/wf_list_tr.csv) | 40,709 | 2,510 |
| [Finnish](wf_lists/wf_list_fi.csv) | 41,035 | 2,497 |
| [Norwegian](wf_lists/wf_list_no.csv) | 18,497 | 2,370 |
| [Hebrew](wf_lists/wf_list_he.csv) | 30,626 | 2,358 |
| [Icelandic](wf_lists/wf_list_is.csv) | 28,171 | 2,358 |
| [Catalan](wf_lists/wf_list_ca.csv) | 23,128 | 2,355 |
| [Latvian](wf_lists/wf_list_lv.csv) | 34,425 | 2,345 |
| [Galician](wf_lists/wf_list_gl.csv) | 25,358 | 2,196 |
| [Bulgarian](wf_lists/wf_list_bg.csv) | 30,254 | 2,189 |
| [Macedonian](wf_lists/wf_list_mk.csv) | 27,053 | 2,186 |
| [Bosnian](wf_lists/wf_list_bs.csv) | 33,845 | 2,185 |
| [Croatian](wf_lists/wf_list_hr.csv) | 33,920 | 2,178 |
| [Albanian](wf_lists/wf_list_sq.csv) | 21,033 | 2,178 |
| [Ukrainian](wf_lists/wf_list_uk.csv) | 37,264 | 2,178 |
| [Tagalog](wf_lists/wf_list_tl.csv) | 14,169 | 2,176 |
| [Urdu](wf_lists/wf_list_ur.csv) | 9,822 | 2,175 |
| [Slovak](wf_lists/wf_list_sk.csv) | 37,801 | 2,172 |
| [Romanian](wf_lists/wf_list_ro.csv) | 24,237 | 2,170 |
| [Czech](wf_lists/wf_list_cs.csv) | 38,489 | 2,169 |
| [Lithuanian](wf_lists/wf_list_lt.csv) | 35,363 | 2,169 |
| [Esperanto](wf_lists/wf_list_eo.csv) | 23,034 | 2,166 |
| [Estonian](wf_lists/wf_list_et.csv) | 33,325 | 2,165 |
| [Slovenian](wf_lists/wf_list_sl.csv) | 33,631 | 2,161 |
| [Serbian](wf_lists/wf_list_sr.csv) | 45,632 | 2,159 |
| [Georgian](wf_lists/wf_list_ka.csv) | 29,020 | 2,147 |
| [Basque](wf_lists/wf_list_eu.csv) | 22,421 | 2,146 |
| [Malay](wf_lists/wf_list_ms.csv) | 11,868 | 2,114 |
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